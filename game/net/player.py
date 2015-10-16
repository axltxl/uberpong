# -*- coding: utf-8 -*-

"""
game.net.player
~~~~~~~~
Client implementation for a player

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import pyglet
import time
import ming

from engine.spot import spot_set, spot_get
from .scene import Scene
from . import (
    Packet,
    Request,
    Response
)


class PlayerClient(ming.Client):
    """
    Player client implementation
    """

    def __init__(self, *, ball_position, **kwargs):
        """Constructor

        Kwargs:
            ball_position(int,int): ball initial position
            kwargs(dict, optional): Arbitrary keyword arguments
        """

        # Call the parent
        super().__init__(**kwargs)

        # This will hold the UUID assigned by a server
        # and used on further requests
        self._id = None

        # base image
        self._img = pyglet.image.load('assets/images/glasspaddle2.png')

        # paddle image region
        paddle_width, paddle_height = spot_get('paddle_size')
        self._paddle_region = self._img.get_region(0, 0, paddle_width, paddle_height)

        # centered anchor as required by pymunk bodies at the server side
        self._paddle_region.anchor_x = self._paddle_region.width // 2
        self._paddle_region.anchor_y = self._paddle_region.height // 2

        # ball image region
        ball_width, ball_height = spot_get('ball_size')
        self._ball_region = self._img.get_region(0, 0, ball_width, ball_height)

        # centered anchor as required by pymunk bodies at the server side
        self._ball_region.anchor_x = self._ball_region.width // 2
        self._ball_region.anchor_y = self._ball_region.height // 2

        # sprites
        self._paddle_me_sprite = pyglet.sprite.Sprite(self._paddle_region)
        self._paddle_foe_sprite = pyglet.sprite.Sprite(self._paddle_region)
        self._ball_sprite = pyglet.sprite.Sprite(self._ball_region)

        # Sprites are invisible at first
        self._paddle_me_sprite.visible = False
        self._paddle_foe_sprite.visible = False
        self._ball_sprite.visible = False

        # paddles initial position
        self._paddle_me_x = 0
        self._paddle_me_y = 0
        self._paddle_foe_x = 0
        self._paddle_foe_y = 0

        # ball position
        self._ball_x, self._ball_y = ball_position

        # paddles initial velocity
        self._paddle_me_vx = 0
        self._paddle_me_vy = 0
        self._paddle_foe_vx = 0
        self._paddle_foe_vy = 0

        # ball velocity
        self._ball_vx = 0
        self._ball_vy = 0

        # Whether the client has succesfully connected to a server
        self._me_connected = False

        # Whether a foe player is present in the game
        self._foe_connected = False

        # Whether the client is currently pressing up or down keys
        self._key_move_up = False
        self._key_move_down = False

        # Time scale (for in-client physics)
        self._current_time = time.time()
        self._dt = 0.0  # time delta

        # Command rate
        # How much command is this client going to send per second?
        self._cmdrate = 1.0 / spot_get('cl_cmdrate')
        pyglet.clock.schedule_interval(self.send_commands, self._cmdrate)

        # Updates frequence
        # Set up updates interval on client
        self._update_lock = False # if True, this client will ignore any incoming data
        self._update_rate = 1.0 / spot_get('cl_updaterate')
        pyglet.clock.schedule_interval(self.update_from_server, self._update_rate)

        # Initial state on server
        self._server_state = None

        # Ready the player?
        self._key_ready = False

        # scores label
        scores_x, scores_y = spot_get('scores_position')
        self._scores_label = pyglet.text.Label(
            font_name='8-bit Operator+',
            x=scores_x, y=scores_y,font_size=32,
            anchor_x='center', anchor_y='center'
        )

        # scores themselves
        self._score_me = 0
        self._score_foe = 0

    @property
    def connected(self):
        return self._me_connected

    @property
    def server_state(self):
        """Get current state in server"""
        return self._server_state

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


    def disconnect(self):
        """Disconnect from server

        Send a connect request to start handshaking with the server

        =>
            {
                'version': 1,
                'cmd': '-connect',
                'player_id': '25aee061a5f34977bf672d4ff59fdc36'
            }

        """
        self.send(Request(command=Request.CMD_DISCONNECT))


    def send(self, request):
        """Send a regular request to server

        Args:
            request(Request): A regular request object
        """

        # Set player uuid upon request
        if self._me_connected:
            request.player_id = self._id

        # Send request to server
        super().send(request.data)


    def send_commands(self, dt):
        """Send commands to the server"""

        if self.server_state == Scene.ST_PLAYING:
            if self._key_move_up:
                self.send(Request(command=Request.CMD_MV_UP))

            if self._key_move_down:
                self.send(Request(command=Request.CMD_MV_DN))

        if self.server_state == Scene.ST_BEGIN and self._key_ready:
            self.send(Request(command=Request.CMD_READY))
            self._key_ready = False


    def update_from_server(self, dt):
        """See whether something arrives from the server"""

        # Unleash the kraken!
        self._update_lock = False

    def tick(self):
        """Run simulation on client"""

        # Physics are performed based on
        # client prediction based on his last known position
        # and velocity. This is done for consistent client-server
        # physics.

        if self._me_connected:

            # Recalculate time delta
            now = time.time()
            self._dt = now - self._current_time
            self._current_time = now

            # predict ball position on the plane
            if self.server_state != Scene.ST_BEGIN:
                self._ball_x += self._ball_vx * self._dt
                self._ball_y += self._ball_vy * self._dt

            # Set ball position
            self._ball_sprite.set_position(self._ball_x, self._ball_y)

            # predict paddle and ball positions on the plane
            self._paddle_me_y += self._paddle_me_vy * self._dt

            # Set paddle position
            self._paddle_me_sprite.set_position(
                self._paddle_me_x,
                self._paddle_me_y
            )

        #
        # Do all stuff for foe player if connected
        #
        if self._foe_connected:
            # Calculate/predict foe paddle position
            self._paddle_foe_y += self._paddle_foe_vy * self._dt

            # Set paddle position
            self._paddle_foe_sprite.set_position(self._paddle_foe_x, self._paddle_foe_y)

    def draw_scores(self):
        if self._number_me == 1:
            scores_label_format = "{} {}".format(
                    self._score_me,
                    self._score_foe
                    )
        else:
            scores_label_format = "{} {}".format(
                    self._score_foe,
                    self._score_me
                    )
        self._scores_label.text = scores_label_format
        self._scores_label.draw()

    def draw_ball(self):
        """Render the ball"""

        # Draw the thing onto the screen
        self._ball_sprite.draw()


    def draw_paddles(self):
        """Render paddles"""

        # draw sprites
        self._paddle_me_sprite.draw()

        #
        # Do all stuff for foe player if connected
        #
        if self._foe_connected:

            # A foe has connected to the game, so it's time
            # to draw him
            if not self._paddle_foe_sprite.visible:
                self._paddle_foe_sprite.visible = True

            # Draw foe sprite
            self._paddle_foe_sprite.draw()



    def on_data_received(self, data, host, port):
        """Response pump for this client"""

        # The kraken is on a leash! :(
        if self._update_lock:
            return

        # The kraken is on the wild!
        self._update_lock = True

        # Get raw data and get a proper Response from it
        response = Response(data=data)


        ########################################
        # The actual pump
        ########################################

        #
        # Request has been denied
        #
        if response.status == Response.STATUS_UNAUTHORIZED:
            if response.reason == Response.REASON_CONN_REFUSED:
                #
                # Connection has been refused from the server
                #
                raise ConnectionRefusedError(
                    "Connection to {}:{} refused!".format(
                    self._server_addr, self._server_port))

        #
        # A request has been accepted by the server
        #
        if response.status == Response.STATUS_OK:

            if response.reason == Response.REASON_CONN_GRANTED:
                # This player knows he has connected succesfully
                # to the server

                # Assume player id
                self._id = response.player_id

                # Let it be known that this player has hereby connected
                # to a server
                self._me_connected = True

                # Start drawing the ball and this player's paddle
                self._paddle_me_sprite.visible = True
                self._ball_sprite.visible = True

            # Set state found on server
            self._server_state = response.state

            # if 'players' in response.data:
            me = response.get_player_info(name='you')
            if me is not None:
                #
                # Update data used to update the paddle sprite
                #

                # position
                self._paddle_me_x, self._paddle_me_y = me['position']

                # velocity
                self._paddle_me_vx, self._paddle_me_vy = me['velocity']

                # score
                self._score_me = me['score']

                # number
                self._number_me = me['number']

            #
            # Set all information regarding the opponent (foe)
            #
            foe = response.get_player_info(name='foe')
            if foe is not None:

                # Let it be known hereby that the opponent has entered
                # the arena!
                self._foe_connected = True

                # position
                self._paddle_foe_x, self._paddle_foe_y = foe['position']

                # velocity
                self._paddle_foe_vx, self._paddle_foe_vy = foe['velocity']

                # score
                self._score_foe = foe['score']

                # number
                self._number_foe = foe['number']

            else:
                # Oh!, foe is not present in the game
                self._foe_connected = False

            #
            # The actual ball information
            #
            ball = response.get_ball_info()
            if ball is not None:

                # position and current velocity of the ball
                self._ball_x, self._ball_y = ball['position']
                self._ball_vx, self._ball_vy = ball['velocity']



    def on_key_press(self, symbol, modifiers):
        """Send packets to the server as the player hits buttons"""

        if self.server_state == Scene.ST_PLAYING:
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

        if self.server_state == Scene.ST_BEGIN:
            #
            # Ready the player
            #
            self._key_ready = True


    def on_key_release(self, symbol, modifiers):

        if self.server_state == Scene.ST_PLAYING:
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
