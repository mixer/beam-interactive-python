import unittest
from beam_interactive.proto.identifier import identifier
from beam_interactive.proto.tetris_pb2 import Handshake
from beam_interactive.proto.rw import Reader

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
        reader.push(data)

        for packet in reader:
            decoded, byte = packet
            print(decoded)
