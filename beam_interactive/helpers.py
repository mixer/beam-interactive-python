import asyncio
from .connection import Connection
from .proto import Handshake

@asyncio.coroutine
def start(loop, remote, channel, key):
    """Starts a new Interactive client.

    Takes the remote address of the Tetris robot, as well as the
    channel number and auth key to use. Additionally, it takes
    a list of handler. This should be a dict of protobuf wire
    IDs to handler functions (from the .proto package).
    """

    if isinstance(address, (list, tuple)):
        address = ':'.join(address)

    reader, writer = yield from asyncio.open_unix_connection(
        address, loop=loop)

    conn = Connection(reader, writer)
    conn.send(_create_handshake(channel, key))


def _create_handshake(channel, key):
    """
    Creates and returns a Handshake packet that authenticates
    on the channel with the given stream key.
    """
    hsk = Handshake()
    hsk.channel = channel
    hsk.key = key
    return hsk
