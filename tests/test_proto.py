import unittest
import random
from beam_interactive.proto.identifier import identifier
from beam_interactive.proto.tetris_pb2 import Handshake, Error
from beam_interactive.proto.rw import Reader, Writer

class Foo():
    pass

def read(fixture):
    with open('tests/fixture/%s' % fixture, mode='rb') as file:
        return file.read()

class TestIdentifierProto(unittest.TestCase):

    def test_identifies_id_for_packet(self):
        self.assertEqual(0, identifier.get_packet_id(Handshake()))

    def test_identifies_id_for_unk_packet(self):
        self.assertIsNone(identifier.get_packet_id(Foo()))

    def test_gets_class_for_identifier(self):
        self.assertEqual(Handshake, identifier.get_packet_from_id(0))


class TestRw(unittest.TestCase):

    def test_reads_packets(self):
        data = read('hundred_packets')
        reader = Reader()

        pos = 0
        msg = 0
        while pos < len(data):
            read_bytes = random.randint(0, 10)
            reader.push(data[pos:pos+read_bytes])
            pos += read_bytes

            for packet in reader:
                decoded, byte = packet
                self.assertEqual('msg%d' % msg, decoded.message)
                msg += 1

    def test_writes_packets(self):
        expected = read('hundred_packets')
        writer = Writer()
        actual = b''

        for x in range(0, 100):
            err = Error()
            err.message = 'msg%d' % x
            writer.push(err)

            if random.random() < 0.2:
                actual += writer.read()

        actual += writer.read()

        self.assertEqual(expected, actual)

