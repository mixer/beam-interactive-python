from .identifier import identifier
from .varint import varuint_decode, varuint_encode, NotEnoughDataException
from ..exceptions import EncoderException, DecoderException


def encode(packet):
    """Encodes a single packet to a byte string. Returns the byte string."""
    return _Encoder().encode(packet)


def decode(bytes):
    """Attempts to decode the packet from the set of bytes. If the packet
    is not known, this function will return None."""
    return _Decoder().decode(bytes)


class _Decoder():
    """Decodes a single packet off of a byte string."""

    def _read_variunt(self):
        try:
            n, read = varuint_decode(self.buffer, self._pos)
            self._pos = read
            return n
        except NotEnoughDataException:
            raise DecoderException('invalid packet; could not read ID')

    def remaining_bytes(self, meta=True):
        """
        Returns the remaining, unread bytes from the buffer.
        """
        pos, self._pos = self._pos, len(self.buffer)
        return self.buffer[pos:]

    def decode(self, bytes):
        """
        Decodes the packet off the byte string.
        """

        self.buffer = bytes
        self._pos = 0

        Packet = identifier.get_packet_from_id(self._read_variunt())

        # unknown packets will be None from the identifier
        if Packet is None:
            return None

        packet = Packet()
        packet.ParseFromString(self.remaining_bytes())
        return packet


class _Encoder():
    """
    The opposite of Decoder, Encoder helps with writing a packet.
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

    def encode(self, packet):
        """
        Pushes a packet to the writer, encoding it on the internal
        buffer.
        """

        id = identifier.get_packet_id(packet)
        if id is None:
            raise EncoderException('unknown packet')

        self._write_variunt(id)
        self._write(packet.SerializeToString())

        return bytes(self.buffer)
