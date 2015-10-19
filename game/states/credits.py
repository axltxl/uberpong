# -*- coding: utf-8 -*-

"""
game.states.splash
~~~~~~~~
Splash title state

Purpose:
* A nice splash text is drawn here


(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet
from .base import BaseState
from engine.spot import spot_set, spot_get

class CreditsState(BaseState):
    """Game start state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # Title label
        self._title_label = pyglet.text.Label(
            spot_get('game_name'), font_name='8-bit Operator+', font_size=72,
            x=machine.window.width//2, y=machine.window.height//2 + 16,
            anchor_x='center', anchor_y='center'
        )


    def _get_going(self, dt):
        """Switch to next state"""
        self.push('game_load')

    #
    # pyglet event callbacks
    #

    def on_update(self):
        # Draw labels
        self._title_label.draw()
        if self._show_press_start:
            self._comp_label.draw()

