import asyncio
import collections
from websockets.exceptions import ConnectionClosed
from .proto import encode, decode


states = {'open': 0, 'closing': 1, 'closed': 2}


class NoPacketException(Exception):
    """
    This error is thrown when you attempt to get_packet() without
    there being a packet in the queue. Instead, you should wait
    using wait_message().
    """
    pass


class Connection():
    """
    This is used to interface with the Tetris Robot client. It
    provides methods for reading data as well as pushing protobuf
    packets on.

    Much of the functionality here is inspired by aioredis. Kudos
    to them for supplementing my woefully lacking knowledge of
    Python concurrency features. You can check them out here:
    https://github.com/aio-libs/aioredis
    """

    def __init__(self, socket, loop):
        self._socket = socket
        self._loop = loop
        self._state = states['open']

        self._read_task = asyncio.Task(self._read_data(), loop=loop)
        self._read_queue = collections.deque()
        self._read_waiter = None

    def _push_packet(self, packet):
        """
        Appends a packet to the internal read queue, or notifies
        a waiting listener that a packet just came in.
        """
        self._read_queue.append((decode(packet), packet))

        if self._read_waiter is not None:
            w, self._read_waiter = self._read_waiter, None
            w.set_result(None)

    @asyncio.coroutine
    def _read_data(self):
        """
        Reads data from the connection and adds it to _push_packet,
        until the connection is closed or the task in cancelled.
        """
        while True:
            try:
                data = yield from self._socket.recv()
            except asyncio.CancelledError:
                break
            except ConnectionClosed:
                break

            self._push_packet(data)

        self._loop.call_soon(self.close)

    @asyncio.coroutine
    def wait_message(self):
        """
        Waits until a connection is available on the wire, or until
        the connection is in a state that it can't accept messages.
        It returns True if a message is available, False otherwise.
        """
        if self._state != states['open']:
            return False
        if len(self._read_queue) > 0:
            return True

        assert self._read_waiter is None or self._read_waiter.cancelled(), \
            "You may only use one wait_message() per connection."

        self._read_waiter = asyncio.Future(loop=self._loop)
        yield from self._read_waiter
        return self.wait_message()

    def get_packet(self):
        """
        Returns the last packet from the queue of read packets.
        If there are none, it throws a NoPacketException.
        """
        if len(self._read_queue) == 0:
            raise NoPacketException()

        return self._read_queue.popleft()

    @asyncio.coroutine
    def send(self, packet):
        """
        Sends a packet to the Interactive daemon over the wire.
        """
        yield from self._socket.send(encode(packet))

    def _do_close(self):
        """
        Underlying closer function.
        """

        self._socket.close()
        self._state = states['closed']

    def close(self):
        """
        Closes the connection if it is open.
        """

        if self._state == states['open']:
            self._do_close()

    @property
    def open(self):
        """
        Returns true if the connection is still open.
        """

        return self._state == states['open']

    @property
    def closed(self):
        """
        Returns true if the connection is closed, or
        in the process of closing.
        """

        return not self.open
