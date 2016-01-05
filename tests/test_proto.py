import unittest
import random

from beam_interactive.proto.identifier import identifier
from beam_interactive.proto.tetris_pb2 import Handshake, Error
from beam_interactive.proto.rw import encode, decode
from beam_interactive.exceptions import EncoderException, DecoderException

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

    def test_provides_magic_attrs(self):
        self.assertEqual(0, identifier.handshake)
        self.assertEqual(1, identifier.handshake_ack)
        with self.assertRaises(AttributeError):
            identifier.handshake_ackasdf


class TestCoders(unittest.TestCase):

    def test_decodes(self):
        data = decode(read('a_packet'))
        self.assertIsInstance(data, Error)
        self.assertEqual('msg0', data.message)

    def test_decode_throws_on_incomplete(self):
        with self.assertRaises(DecoderException): decode([0xf3])
        with self.assertRaises(DecoderException): decode([])

    def test_encode(self):
        err = Error()
        err.message = 'msg0'
        self.assertEqual(read('a_packet'), encode(err))

    def test_encode_throws_on_invalid(self):
        with self.assertRaises(EncoderException): encode(Foo())

