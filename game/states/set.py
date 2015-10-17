# -*- coding: utf-8 -*-

"""
game.states.score
~~~~~~~~
A player has scored

Purpose:
* Declare a winner with celebration and everything!
* Ask each player whether they want another round,
  if so, the game rewinds to BeginState, otherwise,
  the game ends.

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

from engine.state import State
from engine.spot import spot_set, spot_get

from ..net import Scene

class GameSetState(State):
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

    def _go_back(self, dt):
        if self._server is not None:
            # TODO: horrible workaround
            self._server._state = Scene.ST_BEGIN
        self.pop_until('game_begin')

    def on_begin(self):
        pyglet.clock.schedule_once(self._go_back, 3)

    def on_exit(self):
        pass

    def on_update(self):
        pass
