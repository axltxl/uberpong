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
    def __init__(self, *, position, **kwargs):
        """Constructor"""
        super().__init__(**kwargs)

        # This will hold the UUID assigned by a server
        # and used on further requests
        self._id = None

        # TODO: document all of this

        # base image
        self._img = pyglet.image.load('assets/images/glasspaddle2.png')

        # image region
        self._ball_region = self._img.get_region(0, 0, 32, 64)

        # anchor
        self._ball_region.anchor_x = self._ball_region.width // 2
        self._ball_region.anchor_y = self._ball_region.height // 2


        # sprite
        self._sprite = pyglet.sprite.Sprite(self._ball_region)


        # position
        self._x, self._y = position

        # velocity
        self._vx = 0
        self._vy = 0

        # connection flag
        # TODO: document this
        self._connected = False

        # TODO: document this
        self._key_move_up = False
        self._key_move_down = False

    def connect(self):
        """Connect to server

        Send a connect request to start handshaking with the server

        =>
            {
                'version': 1,
                'cmd': '+connect'
            }

        """
        self.send(Request(command=Request.CMD_CONNECT))

    def send(self, request):
        """Send a regular request to server

        Args:
            request(Request): A regular request object
        """

        # Set player uuid upon request
        if self._connected:
            request.player_id = self._id

        # Send request to server
        super().send(request.data)

    def pump(self):

        if self._key_move_up:
            self.send(Request(command=Request.CMD_MV_UP))

        if self._key_move_down:
            self.send(Request(command=Request.CMD_MV_DN))

        # Pump netowrk traffic!
        super().pump()

    def draw(self):
        # TODO: document this
        # fixed time as used in server side
        # use SPOT var 'timestep' instead
        self._x += self._vx * 1/60.0
        self._y += self._vy * 1/60.0

        # Set position
        self._sprite.set_position(self._x, self._y)

        # draw sprite
        self._sprite.draw()

        # update
        # TODO: DOCUMENT THIS!
        # IT IS IMPORTANT TO LET KNOW HOW THIS HAS
        # AN IMPORTANT INFLUENCE ON SERVER-SIDE
        # THESIS: DON'T FLOOD THE SERVER WITH UPDATES
        # STILL KINDA BUGGY, SOMETIMES IT NEEDS TO UPDATE
        # WITHOUT ANY USER INTERVENTION, FIND OUT THE BEST
        # WAY
        if self._key_move_up or self._key_move_down:
            if self._connected:
                self.send(Request(command=Request.CMD_UPDATE))

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
                    self._server_addr, self._server_port))

        if response.status == Response.STATUS_OK:

            # TODO: document this
            if not self._connected:
                self._connected = True

            # TODO: and this as well
            if 'players' in response.data:
                #
                # Update data used to update the paddle sprite
                #

                # FIXME: do something better than this!
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
        # move up
        #
        if symbol == pyglet.window.key.W:
            self._key_move_up = True

        #
        # move down
        #
        if symbol == pyglet.window.key.S:
            self._key_move_down = True


    def on_key_release(self, symbol, modifiers):

        #
        # move up
        #
        if symbol == pyglet.window.key.W:
            self._key_move_up = False

        #
        # move down
        #
        if symbol == pyglet.window.key.S:
            self._key_move_down = False
