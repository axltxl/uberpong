# -*- coding: utf-8 -*-

"""
ming.server
~~~~~~~~
Server implementation

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

from .channel import Channel


class Server(Channel):
    """
    Network server implementation
    """
    def __init__(self, *, port, **kwargs):
        """Constructor"""
        super().__init__(**kwargs)

        # Bind socket to port
        self.sock.bind(("", port))

    def send_default(self, data, host, port):
        self.send({
            "src_addr": host,
            "src_port": port,
            "data": data,
        }, host, port)

    def on_data_received(self, data, host, port):
        self.send_default(data, host, port)
