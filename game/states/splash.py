# -*- coding: utf-8 -*-

"""
game.states.splash
~~~~~~~~
Splash title state

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet
from engine.state import State
from engine.spot import spot_set, spot_get

class GameSplash(State):
    """Game start state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # Toggle flags
        self._show_press_start = True  # This is used for _comp_label animation
        self._key_pressed = False  # has been a key pressed?

        # This should be moved to another level
        pyglet.font.add_file('assets/fonts/8bitOperatorPlus-Regular.ttf')
        font_8bit_operator = pyglet.font.load('8-bit Operator+')

        # and this as well
        self.snd_begin = pyglet.media.load('assets/sounds/begin.wav', streaming=False)

        # Title label
        self._title_label = pyglet.text.Label(
            spot_get('game_name'), font_name='8-bit Operator+', font_size=72,
            x=machine.window.width//2, y=machine.window.height//2 + 16,
            anchor_x='center', anchor_y='center'
        )

        # Companion label
        self._comp_label = pyglet.text.Label(
            "Press ANY KEY to play!", font_name='8-bit Operator+', font_size=24,
            x=machine.window.width//2, y=machine.window.height//2 - 64,
            anchor_x='center', anchor_y='center'
        )


    def _toggle_press_start(self, dt):
        """Toggle _show_press_start flag"""
        self._show_press_start ^= True

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


    def on_key_press(self, sym, mod):
        if self._key_pressed:
            return

        pyglet.clock.unschedule(self._toggle_press_start)
        self._key_pressed = True
        self._show_press_start = False

        #
        self.snd_begin.play()
