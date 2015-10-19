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
from .base import FONT_PRIMARY, FONT_SECONDARY
from .. import colors


class SplashState(BaseState):
    """Game start state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine, fade_in=True)

        # base image
        # TODO: replace with soe\mething better!
        self._img = pyglet.image.load('assets/images/sprites.png')

        # logo sprite
        _logo_region = self._img.get_region(96, 0, 464, 256)
        _logo_region.anchor_x = _logo_region.width // 2
        _logo_region.anchor_y = _logo_region.height // 2
        self._logo_sprite = pyglet.sprite.Sprite(_logo_region)
        self._logo_sprite.set_position(
            self.window.width // 2,
            self.window.height // 2
        )

        # Toggle flags
        self._show_press_start = True  # This is used for _comp_label animation
        self._key_pressed = False  # has been a key pressed?

        # and this as well
        self.snd_begin = self.sorcerer.create_sound(
                'snd_begin',
                file_name='begin.wav'
        )

        # Companion label
        self._comp_label = self.create_label(
            "Press ANY KEY to play!",
            font_size=24,
            font_name=FONT_SECONDARY,
            y=32,
            anchor_y='baseline'
        )
        self._comp_label.set_style('color', colors.GRAY0 + (255,))

        # Github label
        self._github_label = self.create_label(
            "github.com/axltxl/pong",
            font_size=18,
            font_name=FONT_SECONDARY,
            anchor_x='right', anchor_y='top',
            y = self.window.height - 8, x = self.window.width - 8
        )
        self._github_label.set_style('color', colors.GRAY0 + (255,))

        # set the background color
        self.set_background_color(*colors.LIGHT_BLUE)


    def _toggle_press_start(self, dt):
        """Toggle _show_press_start flag"""
        self._show_press_start ^= True


    def _get_going(self, dt):
        """Switch to next state"""
        self.transition_to('game_load')


    #
    # pyglet event callbacks
    #

    def on_begin(self):
        pyglet.clock.schedule_interval(self._toggle_press_start, 0.5)


    def on_update(self):
        # Draw labels
        self._github_label.draw()
        self._logo_sprite.draw()
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
