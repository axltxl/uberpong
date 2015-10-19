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
from engine.spot import spot_set, spot_get

from .base import BaseState

class SplashState(BaseState):
    """Game start state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine, fade_in=True)

        # Toggle flags
        self._show_press_start = True  # This is used for _comp_label animation
        self._key_pressed = False  # has been a key pressed?

        # This should be moved to another level
        pyglet.font.add_file('assets/fonts/8bitOperatorPlus-Regular.ttf')
        font_8bit_operator = pyglet.font.load('8-bit Operator+')

        # and this as well
        self.snd_begin = pyglet.media.load('assets/sounds/begin.wav')

        # Title label
        self._title_label = self.create_label(
            spot_get('game_name'), font_size=72,
            y=machine.window.height//2 + 16,
        )

        # Companion label
        self._comp_label = self.create_label(
            "Press ANY KEY to play!", font_size=24,
            y=machine.window.height//2 - 64,
        )


    def _toggle_press_start(self, dt):
        """Toggle _show_press_start flag"""
        self._show_press_start ^= True

    def _get_going(self, dt):
        """Switch to next state"""
        self.push('game_load')

    #
    # pyglet event callbacks
    #

    def on_begin(self):
        pyglet.clock.schedule_interval(self._toggle_press_start, 0.5)


    def on_update(self):
        # Draw labels
        self._title_label.draw()
        if self._show_press_start:
            self._comp_label.draw()

        # draw things on my dad
        super().on_update()


    def on_key_press(self, sym, mod):
        # Evade key redundancy
        if self._key_pressed:
            return

        # Stop "press start" animation
        pyglet.clock.unschedule(self._toggle_press_start)
        self._key_pressed = True
        self._show_press_start = False

        # Play begin sound
        self.snd_begin.play()

        # Schedule a new state onto the stack after the sound has been played
        pyglet.clock.schedule_once(self._get_going, self.snd_begin.duration + 1)
