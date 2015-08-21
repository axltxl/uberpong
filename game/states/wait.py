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

from ..net import Scene

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

        # Server label
        self._wait_label = pyglet.text.Label(
            "Waiting for players to join ...",
            font_name='8-bit Operator+', font_size=14,
            x=machine.window.width//2, y=machine.window.height - 48,
            anchor_x='center', anchor_y='center'
        )

    #
    # pyglet event callbacks
    #

    def on_begin(self):
        pass

    def on_exit(self):
        pass

    def on_update(self):
        self._wait_label.draw()

        if self._client.server_state == Scene.ST_BEGIN:
            self.push('game_begin') # TEMP
