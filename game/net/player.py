# -*- coding: utf-8 -*-

"""
game.net.player
~~~~~~~~
Client implementation for a player

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import pyglet
from engine.spot import spot_set, spot_get
from engine.net import Client
from game.net.packet import Packet, Request, Response


class PlayerClient(Client):
    """
    Player client implementation
    """

    def __init__(self, *, paddle_position, ball_position, **kwargs):
        """Constructor

        Args:
            paddle_position(int,int): paddle initial position
            ball_position(int,int): ball initial position
        """

        #
        super().__init__(**kwargs)

        # This will hold the UUID assigned by a server
        # and used on further requests
        self._id = None

        # base image
        self._img = pyglet.image.load('assets/images/glasspaddle2.png')

        # paddle image region
        w, h = spot_get('paddle_size')
        self._paddle_region = self._img.get_region(0, 0, w, h)

        # centered anchor as required by pymunk bodies at the server side
        self._paddle_region.anchor_x = self._paddle_region.width // 2
        self._paddle_region.anchor_y = self._paddle_region.height // 2

        # ball image region
        w, h = spot_get('ball_size')
        self._ball_region = self._img.get_region(0, 0, w, h)

        # centered anchor as required by pymunk bodies at the server side
        self._ball_region.anchor_x = self._ball_region.width // 2
        self._ball_region.anchor_y = self._ball_region.height // 2

        # sprites
        self._paddle_sprite = pyglet.sprite.Sprite(self._paddle_region)
        self._ball_sprite = pyglet.sprite.Sprite(self._ball_region)

        # paddle position
        self._paddle_x, self._paddle_y = paddle_position

        # ball position
        self._ball_x, self._ball_y = ball_position

        # paddle velocity
        self._paddle_vx = 0
        self._paddle_vy = 0

        # ball velocity
        self._ball_vx = 0
        self._ball_vy = 0

        # Whether the client has succesfully connected to a server
        self._connected = False

        # Whether the client is currently pressing up or down keys
        self._key_move_up = False
        self._key_move_down = False

        # Time scale (for in-client physics)
        self._timescale = spot_get('timescale')

        # Ask the server for updates every cl_update_interval seconds
        # This syncs physics between client and server
        # without needing to flood the server on each tick
        pyglet.clock.schedule_interval(
            self._update,
            spot_get('cl_update_interval')
            )


    def _update(self, dt):
        """Send an update request

        =>
            {
                'version': 1,
                'cmd': 'update',
                'player_id': '78f7ddd8a979ghf98sdf87'
            }

        """
        if self._connected:
            self.send(Request(command=Request.CMD_UPDATE))


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
        """Pump network traffic and toggle key flags"""
        if self._key_move_up:
            self.send(Request(command=Request.CMD_MV_UP))

        if self._key_move_down:
            self.send(Request(command=Request.CMD_MV_DN))

        # Pump network traffic!
        super().pump()


    def draw(self):
        """Render all the things!"""

        # Physics are performed based on a fixed time step
        # or time scale from which all bodies on a scene
        # are ruled. This is done for consistent client-server
        # physics.

        # predict paddle and ball positions on the plane
        self._paddle_x += self._paddle_vx * self._timescale
        self._paddle_y += self._paddle_vy * self._timescale
        self._ball_x += self._ball_vx * self._timescale
        self._ball_y += self._ball_vy * self._timescale

        # Set paddle position
        self._paddle_sprite.set_position(self._paddle_x, self._paddle_y)

        # Set ball position
        self._ball_sprite.set_position(self._ball_x, self._ball_y)

        # draw sprites
        self._paddle_sprite.draw()
        self._ball_sprite.draw()


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

            # This player knows he has connected succesfully
            # to the server
            if not self._connected:
                self._connected = True

            if 'players' in response.data:
                #
                # Update data used to update the paddle sprite
                #
                me = response.get_player_info(name='you')

                # position
                position = me['position']
                self._paddle_x, self._paddle_y = position['x'], position['y']

                # velocity
                velocity = me['velocity']
                self._paddle_vx, self._paddle_vy = velocity['x'], velocity['y']

            if 'ball' in response.data:
                ball = response.data['ball']
                position = ball['position']
                velocity = ball['velocity']

                self._ball_x, self._ball_y = position['x'], position['y']
                self._ball_vx, self._ball_vy = velocity['x'], velocity['y']


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
