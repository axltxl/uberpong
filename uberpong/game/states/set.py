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

from .. import colors
from .base import BaseState
from ..net import Scene


class GameSetState(BaseState):
    """Game begin state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # Title label
        self._gameset_label = self.create_label('Game set!', font_size=100)
        self._gameset_label.set_style('color', colors.GRAY1 + (255,))

        # score sound
        self._snd_gameset = self.sorcerer.create_sound(
            'snd_gameset',
            file_name='Jingle_Win_00.wav'
        )

        # a player to have better sound playback
        self._player = pyglet.media.Player()

    #
    # pyglet event callbacks
    #

    def _go_back(self, dt):
        if self._server is not None:
            # TODO: horrible workaround
            self._server._state = Scene.ST_BEGIN
        self.pop_until('game_begin')

    def on_begin(self):
        # play the damn sound!
        if not self._player.playing:
            self._player.queue(self._snd_gameset)
            self._player.play()

        self.set_background_color(*colors.TURQUOISE)
        pyglet.clock.schedule_once(
            self._go_back, self._snd_gameset.duration + 2
        )

    def on_update(self):
        self._gameset_label.draw()
