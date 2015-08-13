# -*- coding: utf-8 -*-

import socket
import json
import sys
import lz4

NET_MAX_BYTES = 512
NET_ENCODING = 'utf-8'


class Channel:
    """
    UDP data flow unit
    """
    def __init__(self):
        """Constructor"""
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
                data_str = lz4.uncompress(data_raw).decode(NET_ENCODING)
            else:
                data_str = data_raw.decode(NET_ENCODING)
            data = json.loads(data_str)
        except Exception:
            pass

        # on_data_received is only called if data is not empty
        if type(data) is dict and len(data):
            self.on_data_received(data, addr[0], addr[1])

    def send(self, data, host, port):
        """Send raw data through a socket"""
        if type(data) is not dict:
            raise TypeError("data must be a dictionary")

        # Getting raw data
        if self._use_lz4:
            data_raw = lz4.compress(bytes(json.dumps(data), NET_ENCODING))
        else:
            data_raw = bytes(json.dumps(data), NET_ENCODING)

        # Put the data on the wire as an UTF-8 JSON string
        self.sock.sendto(data_raw, (host, port))

    def close(self):
        """Close socket"""
        if self.sock:
            self.sock.close()

    def on_data_received(self, data, host, port):
        pass


class Client(Channel):
    """
    Network client implementation
    """
    def __init__(self, *, host='localhost', port):
        """Constructor"""
        super().__init__()
        self._server_host = host
        self._server_port = port

    def send(self, data):
        """Send raw data to the server"""
        super().send(data, self._server_host, self._server_port)


class Server(Channel):
    """
    Network server implementation
    """
    def __init__(self, *, port):
        """Constructor"""
        super().__init__()
        self.sock.bind(("", port))

    def send_default(self, data, host, port):
        self.send({
            "src_addr": host,
            "src_port": port,
            "data": data,
        }, host, port)

    def on_data_received(self, data, host, port):
        self.send_default(data, host, port)
