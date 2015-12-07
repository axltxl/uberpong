# -*- coding: utf-8 -*-

"""
game.states.wait
~~~~~~~~
Wait for both players to be connected with the server

Purpose:
* To wait for both players to be connected.
  The server will tell when that happens,
  if so, a BeginState is pushed.

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


from .base import BaseState
from .. import colors
from ..net import Scene


class WaitState(BaseState):
    """Game wait state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine, fade_in=False)

        # Server label
        self._wait_label = self.create_label(
            "Waiting for your opponent ...",
            font_size=24,
        )
        self._wait_label.set_style('color', colors.GRAY1 + (255,))

        # set the background color
        self.set_background_color(*colors.PURPLE)

    #
    # pyglet event callbacks
    #

    def on_update(self):
        # Draw label
        self._wait_label.draw()

        # Go to begin state
        if self._client.server_state == Scene.ST_BEGIN:
            self.push('game_begin')

        # draw things on my dad
        super().on_update()
