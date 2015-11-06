from .tetris_pb2 import Handshake, HandshakeACK, Report, Error, ProgressUpdate

_default_packets = [
    {'name': 'handshake', 'cls': Handshake, 'id': 0},
    {'name': 'handshake_ack', 'cls': HandshakeACK, 'id': 1},
    {'name': 'report', 'cls': Report, 'id': 2},
    {'name': 'error', 'cls': Error, 'id': 3},
    {'name': 'progress_update', 'cls': ProgressUpdate, 'id': 4},
]


class _Identifier():
    """
    identifier is used for looking up classes from packet IDs
    and vise versa. Additionally, it provides magic attributes
    that look up the ID of packets by their name. For example,
    `identifier.error` => 3.
    """

    def __init__(self, packets=_default_packets):
        self._packets = packets

    def get_packet_id(self, packet):
        """
        Returns the ID of a protocol buffer packet. Returns None
        if no ID was found.
        """

        for p in self._packets:
            if isinstance(packet, p['cls']):
                return p['id']

        return None

    def get_packet_from_id(self, id):
        """
        Returns the class for a protocol buffer packet having
        the given ID. Returns Nonw if one was not found.
        """

        for packet in self._packets:
            if packet['id'] == id:
                return packet['cls']

        return None

    def __getattr__(self, name):
        """
        Generic getter that can look up packet IDs by their name.
        """

        for packet in self._packets:
            if packet['name'] == name:
                return packet['id']

        raise AttributeError


identifier = _Identifier()
