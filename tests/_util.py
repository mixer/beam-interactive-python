import unittest
import asyncio
import websockets
from functools import wraps


def run_until_complete(fun):
    if not asyncio.iscoroutinefunction(fun):
        fun = asyncio.coroutine(fun)

    @wraps(fun)
    def wrapper(test, *args, **kw):
        loop = test.loop
        ret = loop.run_until_complete(
            asyncio.wait_for(fun(test, *args, **kw), 5, loop=loop))
        return ret
    return wrapper


class EchoServer():

    def __init__(self, loop, host, port):
        self.loop = loop
        self.host = host
        self.port = port

    def start(self):
        return websockets.serve(self._echo, self.host, self.port, loop=self.loop)

    @asyncio.coroutine
    def _echo(self, socket, addr):
        self.socket = socket
        while True:
            try:
                msg = yield from socket.recv()
                yield from socket.send(msg)
            except ConnectionClosed:
                break

    @asyncio.coroutine
    def close(self):
        yield from self.socket.close()


class AsyncTestCase(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.server = None
        asyncio.set_event_loop(None)
        self.echo = self.make_echo_server()

    def tearDown(self):
        if self.server is not None:
            yield from self.server.close()

        self.loop.close()
        del self.loop

    def make_echo_server(self):
        """
        Creates and returns the 'wss://host:port' of a basic websocket echo
        server.
        """
        addr = ('127.0.0.1', 8888)
        self.server = EchoServer(self.loop, addr[0], addr[1])
        self.loop.run_until_complete(self.server.start())

        return 'ws://%s:%s' % addr
