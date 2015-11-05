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
            asyncio.wait_for(fun(test, *args, **kw), 15, loop=loop))
        return ret
    return wrapper


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
        server. This function is taken basically straight from
        the Python docs.
        """
        @asyncio.coroutine
        def handle_echo(reader, writer):
            data = yield from reader.read(100)
            writer.write(data)
            yield from writer.drain()
            writer.close()

        addr = ('127.0.0.1', 8888)
        coro = asyncio.start_server(handle_echo,
            addr[0], addr[1], loop=self.loop)
        self.server = self.loop.run_until_complete(coro)

        return addr
