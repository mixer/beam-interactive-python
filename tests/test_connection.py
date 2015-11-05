from ._util import AsyncTestCase, run_until_complete
from beam_interactive import start

class TestConnection(AsyncTestCase):

    @run_until_complete
    def test_handshakes(self):
        conn = yield from start(self.echo, 42, 'asdf', loop=self.loop)
        yield from conn.wait_message()
        decoded, bytes = conn.get_packet()

        self.assertEqual(42, decoded.channel)
        self.assertEqual('asdf', decoded.streamKey)
