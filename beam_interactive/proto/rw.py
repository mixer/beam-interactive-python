from .identifier import identifier
from .varint import varuint_decode, varuint_encode, NotEnoughDataException


class _DecoderFailedException(Exception):
    pass


class _Decoder():
    """Decodes a single packet off of a byte string."""
    def __init__(self, buffer):
        self._start = 0
        self._buffer = buffer

        self._size = self._read_variunt()
        self._id = self._read_variunt()

    def _read_variunt(self):
        try:
            n, read = varuint_decode(self._buffer, self._start)
            self._start = read
            return n
        except NotEnoughDataException:
            return None

    def has_data(self):
        """
        Returns true if the decoder has enough data to read the
        entire packet.
        """
        # these will have been set to None on initialize if
        # they were incomplete.
        return self._id is not None \
            and self._size is not None \
            and len(self._buffer) - self._start >= self._size

    def is_known(self):
        """
        Returns whether the ID of this a known a decodable ID.
        """

        return identifier.get_packet_from_id(self._id) is not None

    def total_bytes(self):
        """
        Returns the total number of bytes that made up this packet.
        """
        return self._start + self._size

    def raw_bytes(self, meta=True):
        """
        Returns the raw bytes from the start and end of this packet.
        If meta is true, the metadata (length and packet id) will
        be included.
        """
        if meta:
            start = 0
        else:
            start = self._start

        return self._buffer[start:self._start+self._size]

    def decode(self):
        """
        Decodes the packet off the byte string.
        """

        Packet = identifier.get_packet_from_id(self._id)
        packet = Packet()
        packet.ParseFromString(self.raw_bytes(False))
        return packet



class Reader():
    """
    Reader helps with decoding packets. You can .push() some
    binary data onto it, then .read() a packet off of it, or
    use it as an iterable to read all packets it contains.
    """

    def __init__(self):
        self.buffer = b''

    def push(self, data):
        """
        Appends binary data to the reader.
        """

        self.buffer += data
        return self

    def read(self):
        """
        Attempts to read the next protocol buffer packet off
        of the buffer, along with the raw bytes in a tuple. If
        the packet was unknown, the packet will be None.

        Returns None if there was no complete
        packet waiting to be read.
        """

        decoder = _Decoder(self.buffer)
        if not decoder.has_data():
            return None

        self.buffer = self.buffer[decoder.total_bytes():]

        if not decoder.is_known():
            return (None, decoder.raw_bytes())

        return (decoder.decode(), decoder.raw_bytes())

    def __iter__(self):
        return self

    def __next__(self):
        item = self.read()
        if item is None:
            raise StopIteration

        return item


class Writer():
    """
    The opposite of Reader, Writer helps with writing packets.
    You can .push() packets to it, which are encoded and then
    written to an internal buffer which is read via .read().
    """

    def __init__(self):
        self.buffer = bytearray()

    def _write(self, data):
        if isinstance(data, int):
            self.buffer.append(data)
        else:
            self.buffer.extend(data)

    def _write_variunt(self, number):
        varuint_encode(self._write, number)

    def push(self, packet):
        """
        Pushes a packet to the writer, encoding it on the internal
        buffer.
        """

        id = identifier.get_packet_id(packet)
        if id is None:
            raise Exception('unknown packet')

        encoded = packet.SerializeToString()

        self._write_variunt(len(encoded))
        self._write_variunt(id)
        self._write(encoded)

        return self

    def read(self):
        """
        Returns and consumes all encoded data from the writer.
        """

        buffer, self.buffer = self.buffer, bytearray()
        return buffer


