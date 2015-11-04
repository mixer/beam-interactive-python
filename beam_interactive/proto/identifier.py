from .tetris_pb2 import Handshake, HandshakeACK, Report, Error, ProgressUpdate


class _Identifier():

    def __init__(self):
        self.packets = [
            { 'cls': Handshake, 'id': 0 },
            { 'cls': HandshakeACK, 'id': 1 },
            { 'cls': Report, 'id': 2 },
            { 'cls': Error, 'id': 3 },
            { 'cls': ProgressUpdate, 'id': 4 },
        ]

    def get_packet_id(self, packet):
        """
        Returns the ID of a protocol buffer packet. Returns None
        if no ID was found.
        """

        return next((p['id'] for p in self.packets
            if isinstance(packet, p['cls'])), None)

    def get_packet_from_id(self, id):
        """
        Returns the class for a protocol buffer packet having
        the given ID. Returns Nonw if one was not found.
        """

        return next((p['cls'] for p in self.packets
            if p['id'] == id), None)

identifier = _Identifier()
