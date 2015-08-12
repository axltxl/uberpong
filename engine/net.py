# -*- coding: utf-8 -*-

import socket
import json
import sys

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

    def pump(self):
        """Receive raw data from socket and decode it as a dict"""
        data = {}  # fancy data

        # Extract raw JSON data from socket and
        # convert it into a dict (if possible)
        try:
            data_raw, addr = self.sock.recvfrom(NET_MAX_BYTES)
            data = json.loads(data_raw.decode(NET_ENCODING))
        except Exception:
            pass

        # on_data_received is only called if data is not empty
        if type(data) is dict and len(data):
            self.on_data_received(data, addr[0], addr[1])

    def send(self, data, host, port):
        """Send raw data through a socket"""
        if type(data) is not dict:
            raise TypeError("data must be a dictionary")

        # Put the data on the wire as an UTF-8 JSON string
        self.sock.sendto(bytes(json.dumps(data), NET_ENCODING), (host, port))

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
