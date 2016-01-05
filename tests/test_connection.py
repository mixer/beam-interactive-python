from ._util import AsyncTestCase, run_until_complete
from beam_interactive.proto import Error
from beam_interactive import start

class TestConnection(AsyncTestCase):

    @run_until_complete
    def test_handshakes(self):
        conn = yield from start(self.echo, 42, 'asdf', loop=self.loop)

        self.assertTrue(conn.open)
        self.assertFalse(conn.closed)

        self.assertTrue((yield from conn.wait_message()))
        decoded, bytes = conn.get_packet()
        self.assertEqual(42, decoded.channel)
        self.assertEqual('asdf', decoded.streamKey)

        err = Error()
        err.message = 'foo'
        yield from conn.send(err)
        self.assertTrue((yield from conn.wait_message()))
        decoded, bytes = conn.get_packet()
        self.assertEqual('foo', err.message)

        conn.close()

        self.assertFalse((yield from conn.wait_message()))
        self.assertFalse(conn.open)
        self.assertTrue(conn.closed)

