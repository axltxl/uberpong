# -*- coding: utf-8 -*-

import pyglet.window.key

from engine.net import Client

from game.net.packet import Packet, PacketRequest, PacketResponse

class PlayerClient(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._id = None

    def connect(self):
        request = PacketRequest()
        request.command = PacketRequest.CMD_CONNECT
        self.send(request)

    def send(self, request):
        request.player_id = self._id
        super().send(request.data)

    def on_data_received(self, data, host, port):
        response = PacketResponse(data)

        if response.player_id is not None:
            self._id = response.player_id

        if response.status == PacketResponse.STATUS_UNAUTHORIZED:
            if response.reason == PacketResponse.REASON_CONN_REFUSED:
                raise ConnectionRefusedError(
                    "Connection to {}:{} refused!".format(
                    self._server_host, self._server_port))

    def on_key_press(self, symbol, modifiers):
        """Send packets to the server as the player hits buttons"""

        #
        request = PacketRequest()

        #
        send_pkt = False

        # move up
        if symbol == pyglet.window.key.W:
            request.command = PacketRequest.CMD_MV_UP
            send_pkt = True

        # move down
        elif symbol == pyglet.window.key.S:
            request.command = PacketRequest.CMD_MV_DN
            send_pkt = True

        if send_pkt:
            self.send(request)

    def on_key_release(self, symbol, modifiers):
        pass
