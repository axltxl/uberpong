# -*- coding: utf-8 -*-

from engine.net import Client

class Player(Client):
    def on_data_received(self, data, host, port):
        print(data)

    def on_key_press(self, sym, mod):
        # maybe send packets to the server as the player hits buttons
        self.send({"key": sym, "mod": mod})
