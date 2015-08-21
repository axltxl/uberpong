# -*- coding: utf-8 -*-

"""
game.states.begin
~~~~~~~~
Game begin state

Purpose:
* Set up board
* Reset score count
* Reset players to their original position
* Wait for players to be ready

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
        self._client = spot_get('game_client')

        # Server label
        self._wait_label = pyglet.text.Label(
            "Press any key when you are READY ...",
            font_name='8-bit Operator+', font_size=20,
            x=machine.window.width//2, y=48,
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
        self._client.tick()
        self._client.draw_ball()
        self._client.draw_paddles()
