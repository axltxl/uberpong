# -*- coding: utf-8 -*-

"""
game.states.begin
~~~~~~~~
Game begin state

Purpose:
* Set up board
* Reset score count
* Reset players to their original position

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

from engine.state import State
from engine.spot import spot_set, spot_get


class BeginState(State):
    """Game begin state"""

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
        pass
