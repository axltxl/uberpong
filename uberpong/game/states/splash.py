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

from uberpong import __version__ as pkg_version
from uberpong import PKG_URL as pkg_url
from uberpong.engine.spot import spot_get

from .base import BaseState
from ..net import Packet
from ..utils import FONT_SECONDARY
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
        self._img = self.sorcerer.get_resource('sprite_sheet')

        # logo sprite
        _logo_region = self._img.get_region(96, 0, 464, 256)
        _logo_region.anchor_x = _logo_region.width // 2
        _logo_region.anchor_y = _logo_region.height // 2
        self._logo_sprite = pyglet.sprite.Sprite(_logo_region)
        self._logo_sprite.set_position(
            self.window.width // 2,
            self.window.height // 2
        )

        # ball sprite
        _ball_region = self._img.get_region(32, 32, 64, 64)
        _ball_region.anchor_x = _ball_region.width // 2
        _ball_region.anchor_y = _ball_region.height // 2
        self._ball_sprite = pyglet.sprite.Sprite(_ball_region)
        self._ball_sprite.set_position(
            self._logo_sprite.x + _logo_region.width//2 - 16,
            self.window.height//2 - _logo_region.height//2 + 36
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

        # Github label
        self._github_label = self.create_label(
            pkg_url,
            font_size=16,
            font_name=FONT_SECONDARY,
            anchor_x='right',
            anchor_y='top',
            y=self.window.height-8,
            x=self.window.width-8
        )

        # network text
        net_txt =  "net-{}".format(Packet.PROTO_VERSION)
        if spot_get("argv")['--lz4']:
            net_txt = "{}+lz4".format(net_txt)

        # Version label
        self._version_label = self.create_label(
            "v{} ({})".format(pkg_version, net_txt),
            font_size=14,
            font_name=FONT_SECONDARY,
            anchor_x='left',
            anchor_y='top',
            y=self.window.height-8,
            x=8
        )

        # set the background color
        self.set_background_color(*colors.LIGHT_BLUE)

    def _toggle_press_start(self, dt):
        """Toggle _show_press_start flag"""
        self._show_press_start ^= True

    def _get_going(self, dt):
        """Switch to next state"""
        self.transition_to('game_load')

    def _rotate_ball(self, dt):
        """Rotate the ball"""
        self._ball_sprite.rotation += 2

    #
    # pyglet event callbacks
    #

    def on_begin(self):
        pyglet.clock.schedule_interval(self._toggle_press_start, 0.5)
        pyglet.clock.schedule_interval(self._rotate_ball, 1/60)

    def on_exit(self):
        pyglet.clock.unschedule(self._toggle_press_start)
        pyglet.clock.unschedule(self._rotate_ball)

    def on_update(self):
        # Draw labels
        self._github_label.draw()
        self._version_label.draw()
        if self._show_press_start:
            self._comp_label.draw()

        # Draw sprites
        self._logo_sprite.draw()
        self._ball_sprite.draw()

        # draw things on my dad
        super().on_update()

    def on_key_press(self, sym, mod):
        # ignore F12
        if sym == pyglet.window.key.F12:
            return

        # Evade key redundancy
        if self._key_pressed:
            return

        # Stop text animation
        pyglet.clock.unschedule(self._toggle_press_start)

        # set flags
        self._key_pressed = True
        self._show_press_start = False

        # Play begin sound
        self.snd_begin.play()

        # Schedule a new state onto the stack after the sound has been played
        pyglet.clock.schedule_once(
            self._get_going,
            self.snd_begin.duration + 1
        )
