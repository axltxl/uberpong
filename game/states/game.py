# -*- coding: utf-8 -*-

"""
game.states.game
~~~~~~~~
Game state

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet
from engine.state import State
from engine.spot import spot_set, spot_get

class GameState(State):
    """Game start state"""

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
        pass

    def on_update(self):
        pass

    def on_key_press(self, sym, mod):
        pass
