# -*- coding: utf-8 -*-

"""
game.states.load
~~~~~~~~
Set up client-server

Purpose:
* The client tries to connect to a server
* A nice "Connecting to server..." text is drawn here

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

from ..utils import FONT_SECONDARY
from .base import BaseState
from .. import colors


class LoadState(BaseState):
    """Game start state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine, fade_in=True)

        # A flag to control _get_going
        self._push_schedule = False

        # sprite sheet
        self._img = self.sorcerer.get_resource('sprite_sheet')

        # ball sprite
        _ball_region = self._img.get_region(32, 32, 64, 64)
        _ball_region.anchor_x = _ball_region.width // 2
        _ball_region.anchor_y = _ball_region.height // 2
        self._ball_sprite = pyglet.sprite.Sprite(_ball_region)
        self._ball_sprite.set_position(
            self.window.width // 2,
            self.window.height // 2 + 32
        )

        # Connect label
        self._conn_label = self.create_label(
            "connecting to server...",
            font_size=20, font_name=FONT_SECONDARY,
            x=machine.window.width//2, y=machine.window.height//2 - 16,
        )

        # Server label
        self._server_label = self.create_label(
            "pong://{}:{}".format(
                self._client.server_address, self._client.server_port
            ),
            font_name=FONT_SECONDARY, font_size=32,
            y=machine.window.height//2 - 42,
        )

        # set the background color
        self.set_background_color(*colors.YELLOW)

    #
    # pyglet event callbacks
    #

    def _rotate_ball(self, dt):
        """Rotate the ball"""
        self._ball_sprite.rotation += 2

    def _attempt_connection(self, dt):
        # Attempt to connect to server
        if not self._client.connected:
            self._client.connect()

    def on_exit(self):
        pyglet.clock.unschedule(self._rotate_ball)

    def on_begin(self):
        # rotate the ball
        pyglet.clock.schedule_interval(self._rotate_ball, 1/60)

        #
        # Attemp to vonnect client to server each second
        #
        pyglet.clock.schedule_interval(self._attempt_connection, 1)

    def on_update(self):
        # Draw sprites
        self._ball_sprite.draw()

        #
        # Check whether the client has connected to the server
        #
        if self._client.connected:
            if not self._push_schedule:

                # Tear down connection attempt
                pyglet.clock.unschedule(self._attempt_connection)

                # A flag to control this code block
                self._push_schedule = True

                # get going to next state
                self.transition_to('game_wait')

            # change text on label
            self._server_label.text = 'connected!'

        # Draw labels
        self._conn_label.draw()
        self._server_label.draw()

        # draw things on my dad
        super().on_update()
