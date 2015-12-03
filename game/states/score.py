# -*- coding: utf-8 -*-

"""
game.states.score
~~~~~~~~
A player has scored

Purpose:
* Increase count on winning player
* Check whether one of the players has reached the max score

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


from .base import BaseState
from engine.spot import spot_set, spot_get

from ..net import Scene


class ScoreState(BaseState):
    """Game score state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

    #
    # pyglet event callbacks
    #

    def on_begin(self):
        self.set_background_color(127, 0, 0)

    def on_exit(self):
        pass

    def on_update(self):
        # Draw all the things but the ball in the client!
        self.client.draw_scores()
        self.client.draw_paddles()

        # Switch to previous state
        if self.client.server_state == Scene.ST_PLAYING:
            self.pop()
        elif self.client.server_state == Scene.ST_GAME_SET:
            self.push('game_set')
