# -*- coding: utf-8 -*-

"""
ming.client
~~~~~~~~
Client implementation

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

from .channel import Channel


class Client(Channel):
    """
    Network client implementation
    """

    def __init__(self, *, address='localhost', port, **kwargs):
        """Constructor"""
        super().__init__(**kwargs)

        # Save both server's address and port
        self._server_addr = address
        self._server_port = port

    def send(self, data):
        """Send raw data to the server"""
        super().send(data, self._server_addr, self._server_port)

    @property
    def server_address(self):
        """Get server address"""
        return self._server_addr

    @property
    def server_port(self):
        """Get server port"""
        return self._server_port
