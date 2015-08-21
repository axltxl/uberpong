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

        # Get client
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

    def on_update(self):
        # Draw label
        self._wait_label.draw()

        # Go to begin state
        if self._client.server_state == Scene.ST_BEGIN:
            self.push('game_begin')
