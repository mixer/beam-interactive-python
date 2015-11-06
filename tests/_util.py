import unittest
import asyncio
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


class EchoServer(asyncio.Protocol):
    """
    Based upon:
    https://github.com/python/asyncio/blob/master/examples/tcp_echo.py
    """

    TIMEOUT = 5.0

    def set_loop(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.transport.write(data)

    def eof_received(self):
        pass


class AsyncTestCase(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.server = None
        asyncio.set_event_loop(None)
        self.echo = self.make_echo_server()

    def tearDown(self):
        if self.server is not None:
            self.server.close()
            self.loop.run_until_complete(self.server.wait_closed())

        self.loop.close()
        del self.loop

    def make_echo_server(self):
        """
        Creates and returns the (ip, port) of a basic TCP echo
        server.
        """

        addr = ('127.0.0.1', 8888)
        coro = self.loop.create_server(EchoServer, addr[0], addr[1])
        self.server = self.loop.run_until_complete(coro)

        return addr
