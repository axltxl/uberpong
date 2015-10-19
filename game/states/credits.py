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
        self._title_label = self.create_label('Axel Texel', font_size=18)
        self._presents_label = self.create_label('- presents -',
                font_size=12, y=((self.window.height//2) - 20))
        self._title_label.set_style('color', (240, 240, 240, 255))

        # set the background color
        self.set_background_color(31, 31, 31)


    #
    # pyglet event callbacks
    #

    def on_begin(self):
        # schedule a transition to the next state
        pyglet.clock.schedule_once(self._trans_splash, 2)


    def _trans_splash(self, dt):
        # trigger a transition to the splash state
        self.transition_to('game_splash')


    def on_update(self):
        # Draw labels
        self._title_label.draw()
        self._presents_label.draw()
        super().on_update() # draw things on parent


