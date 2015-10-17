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


import pyglet

from engine.state import State
from engine.spot import spot_set, spot_get

from ..net import Scene

class ScoreState(State):
    """Game score state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # TODO: document this!
        self._server = spot_get('game_server')
        self._client = spot_get('game_client')

    #
    # pyglet event callbacks
    #

    def on_begin(self):
        # Mark score for winning player
        pass

    def on_exit(self):
        pass

    def on_update(self):
        # Draw all the things but the ball in the client!
        self._client.draw_scores()
        self._client.draw_paddles()

        # Switch to previous state
        if self._client.server_state == Scene.ST_PLAYING:
            self.pop()
        elif self._client.server_state == Scene.ST_GAME_SET:
            self.push('game_set')
