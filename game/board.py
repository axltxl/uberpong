# -*- coding: utf-8 -*-

from engine.net import Server

class Board(Server):
    def on_data_received(self, data, host, port):
        self.send(data, host, port)
