import asyncio
from .connection import Connection
from .proto import Handshake


@asyncio.coroutine
def start(address, channel, key, loop=None):
    """Starts a new Interactive client.

    Takes the remote address of the Tetris robot, as well as the
    channel number and auth key to use. Additionally, it takes
    a list of handler. This should be a dict of protobuf wire
    IDs to handler functions (from the .proto package).
    """

    if loop is None:
        loop = asyncio.get_event_loop()

    if isinstance(address, str):
        host, port = address.split(':')
    else:
        host, port = address

    reader, writer = yield from asyncio.open_connection(
        host, port, loop=loop)

    conn = Connection(reader, writer, loop)
    conn.send(_create_handshake(channel, key))

    return conn


def _create_handshake(channel, key):
    """
    Creates and returns a Handshake packet that authenticates
    on the channel with the given stream key.
    """
    hsk = Handshake()
    hsk.channel = channel
    hsk.streamKey = key
    return hsk
