# -*- coding: utf-8 -*-

"""
game.states.wait
~~~~~~~~
The game is set

Purpose:
* To wait for both players to be ready.
  The server will tell when that happens,
  if so, a BeginState is pushed.

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

from engine.state import State
from engine.spot import spot_set, spot_get


class WaitState(State):
    """Game wait state"""

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
