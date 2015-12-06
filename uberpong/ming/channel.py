# -*- coding: utf-8 -*-

"""
ming.core
~~~~~~~~
A series of simple UDP networking utilities

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import socket
import lz4

from .json import JsonCodec
from .ubjson import UbJsonCodec
from .bson import BsonCodec

NET_MAX_BYTES = 512
NET_ENCODING = 'utf-8'


class Channel:
    """
    UDP data flow unit
    """

    CODECS = {
        'json': JsonCodec,
        'bson': BsonCodec,
        'ubjson': UbJsonCodec
    }

    def __init__(self, *, codec='json'):
        """Constructor"""

        #
        if codec.lower() not in self.CODECS:
            raise TypeError('{} is not a valid codec!'.format(codec))

        #
        self._codec = self.CODECS[codec.lower()]()

        # Create the actual UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #########################################################
        # Set the socket to non-blocking mode, so the socket won't
        # have to wait for data on each recvfrom iteration
        #########################################################
        self.sock.setblocking(False)

        # LZ4 compression flag
        self._use_lz4 = False

    @property
    def use_lz4(self):
        """LZ4 compression algorithm flag"""
        return self._use_lz4

    @use_lz4.setter
    def use_lz4(self, value):
        """Activate/deactivate use of LZ4 compression"""
        self._use_lz4 = value

    def pump(self):
        """Receive raw data from socket and decode it as a dict"""
        data = {}  # fancy data

        # Extract raw JSON data from socket and
        # convert it into a dict (if possible)
        try:
            data_raw, addr = self.sock.recvfrom(NET_MAX_BYTES)
            if self._use_lz4:
                data_str = lz4.uncompress(data_raw)
            else:
                data_str = data_raw
            data = self._codec.decode(data_str)
        except Exception as e:
            pass

        # on_data_received is only called if data is not empty
        if (isinstance(data, dict) or isinstance(data, list)) and len(data):
            self.on_data_received(data, addr[0], addr[1])

    def send(self, data, host, port):
        """Send raw data through a socket"""

        if not isinstance(data, dict) and not isinstance(data, list):
            raise TypeError("data must be either a list or a dictionary")

        # Getting raw data
        if self._use_lz4:
            data_raw = lz4.compress(self._codec.encode(data))
        else:
            data_raw = self._codec.encode(data)

        # Put the data on the wire as an UTF-8 JSON string
        self.sock.sendto(data_raw, (host, port))

    def close(self):
        """Close socket"""
        if self.sock:
            self.sock.close()

    def on_data_received(self, data, host, port):
        """This will be called each time a packet arrives"""
        pass
