# -*- coding: utf-8 -*-

"""
game.states.game
~~~~~~~~
Round state

Purpose:
* A game round occurs herein

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

from engine.state import State
from engine.spot import spot_set, spot_get


class RoundState(State):
    """Game round state"""

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
        pass

    def on_exit(self):
        pass

    def on_update(self):
        # Update client!

        self._client.tick()
        self._client.draw_paddles()
        self._client.draw_ball()

        #



    #######################################################
    # All input events are handled directly by the client
    #######################################################

    def on_key_press(self, symbol, modifiers):
        # Update data on client
        self._client.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        # Update data on client
        self._client.on_key_release(symbol, modifiers)