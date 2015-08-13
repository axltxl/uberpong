# -*- coding: utf-8 -*-

from engine.net import Client

from game.net.packet import PacketRequest, PacketResponse

class PlayerClient(Client):
    def connect(self):
        req = PacketRequest()
        req.command = PacketRequest.CMD_CONNECT
        self.send(req.data)

    def on_data_received(self, data, host, port):
        res = PacketResponse(data)

        if res.response == PacketResponse.RES_NOT_OK:
            if res.reason == PacketResponse.REASON_CONN_REFUSED:
                raise ConnectionRefusedError(
                    "Connection to {}:{} refused!".format(
                    self._server_host, self._server_port))

    def on_key_press(self, symbol, modifiers):
        # maybe send packets to the server as the player hits buttons
        self.send({"key": symbol, "mod": modifiers})

    def on_key_release(self, symbol, modifiers):
        self.send({"key": symbol, "mod": modifiers})
