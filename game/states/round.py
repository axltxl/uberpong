# -*- coding: utf-8 -*-

"""
game.states.round
~~~~~~~~
Round state

Purpose:
* A game round occurs herein

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

from engine.spot import spot_set, spot_get

from .base import BaseState
from ..utils import FONT_PRIMARY, FONT_SECONDARY
from .. import colors
from ..net import Scene

class RoundState(BaseState):
    """Game round state"""

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
        if self.server is not None:
            self.server.reset_players()
            self.server.reset_ball()


    def on_update(self):
        # Update client!
        self.client.tick()

        # Draw all the things in the client!
        self.client.draw_board()
        self.client.draw_scores()
        self.client.draw_paddles()
        self.client.draw_ball()

        # Check for a state change, at anytime is expected
        # from the server to change to "score" state
        if self.client.server_state == Scene.ST_SCORE:
            self.push('game_score')


    #######################################################
    # All input events are handled directly by the client
    #######################################################

    def on_key_press(self, symbol, modifiers):
        # Update data on client
        self.client.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        # Update data on client
        self.client.on_key_release(symbol, modifiers)
