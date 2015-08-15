# -*- coding: utf-8 -*-

"""
game.net.player
~~~~~~~~
Client implementation for a player

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import pyglet
from engine.net import Client
from game.net.packet import Packet, Request, Response


class PlayerClient(Client):
    """
    Player client implementation
    """
    def __init__(self, **kwargs):
        """Constructor"""
        super().__init__(**kwargs)

        # This will hold the UUID assigned by a server
        # and used on further requests
        self._id = None

        # sprite
        self._img = pyglet.image.load('assets/images/glasspaddle2.png')
        self._sprite = pyglet.sprite.Sprite(self._img, x=50, y=50)

        # position
        self._x = 0
        self._y = 0

        # velocity
        self._vx = 0
        self._vy = 0

    def connect(self):
        """Connect to server

        Send a connect request to start handshaking with the server

        =>
            {
                'version': 1,
                'cmd': '+connect'
            }

        """
        request = Request()
        request.command = Request.CMD_CONNECT
        self.send(request)

    def send(self, request):
        """Send a regular request to server

        Args:
            request(Request): A regular request object
        """
        request.player_id = self._id  # Set player uuid on request
        super().send(request.data)  # Send request to server


    def draw(self):
        # TODO: document this
        # fixed time as used in server side
        self._x += self._vx * 1/60.0
        self._y += self._vy * 1/60.0

        # Set position
        self._sprite.set_position(self._x, self._y)

        # draw sprite
        self._sprite.draw()

    def on_data_received(self, data, host, port):
        """Response pump for this client"""

        # Get raw data and get a proper Response from it
        response = Response(data)

        # Set player uuid
        if response.player_id is not None:
            self._id = response.player_id

        ########################################
        # The actual pump
        ########################################
        if response.status == Response.STATUS_UNAUTHORIZED:
            if response.reason == Response.REASON_CONN_REFUSED:
                #
                # Connection has been refused from the server
                #
                raise ConnectionRefusedError(
                    "Connection to {}:{} refused!".format(
                    self._server_host, self._server_port))

        if response.status == Response.STATUS_OK:
            if 'players' in response.data:
                #
                # Update data used to update the paddle sprite
                #

                # TODO: do something better than this!
                me = response.data['players']['you']
                position = me['position']
                x = position['x']
                y = position['y']
                self._x, self._y = x, y

                velocity = me['velocity']
                vx = velocity['x']
                vy = velocity['y']
                self._vx, self._vy = vx, vy


    def on_key_press(self, symbol, modifiers):
        """Send packets to the server as the player hits buttons"""

        #
        # Create a new Request
        #
        request = Request()

        #
        # Whether to send the packet or not
        #
        send_pkt = False

        #
        # move up
        #
        if symbol == pyglet.window.key.W:
            request.command = Request.CMD_MV_UP
            send_pkt = True

        #
        # move down
        #
        elif symbol == pyglet.window.key.S:
            request.command = Request.CMD_MV_DN
            send_pkt = True

        if send_pkt:
            self.send(request)

    def on_key_release(self, symbol, modifiers):
        #
        # Create a new Request
        #
        request = Request()

        #
        # Whether to send the packet or not
        #
        send_pkt = False

        #
        # move down
        #
        # if symbol == pyglet.window.key.W:
        #     request.command = Request.CMD_MV_DN
        #     send_pkt = True

        #
        # move up
        #
        # elif symbol == pyglet.window.key.S:
        #     request.command = Request.CMD_MV_UP
        #     send_pkt = True

        if send_pkt:
            self.send(request)
