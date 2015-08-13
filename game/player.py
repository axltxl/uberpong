# -*- coding: utf-8 -*-

from engine.net import Client

class PlayerClient(Client):
    def on_data_received(self, data, host, port):
        print(data)

    def on_key_press(self, symbol, modifiers):
        # maybe send packets to the server as the player hits buttons
        self.send({"key": symbol, "mod": modifiers})

    def on_key_release(self, symbol, modifiers):
        self.send({"key": symbol, "mod": modifiers})
