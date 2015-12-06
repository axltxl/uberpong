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
from .. import colors


class CreditsState(BaseState):
    """Game start state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # create the basic splash sound
        self._snd_credits = self.sorcerer.create_sound(
            'snd_credits',
            file_name='credits.wav'
        )

        # Title label
        self._title_label = self.create_label('Axel Texel', font_size=18)
        self._presents_label = self.create_label(
            '- presents -',
            font_size=12, y=((self.window.height//2) - 20)
        )
        self._title_label.set_style('color', colors.GRAY1 + (255,))
        self._presents_label.set_style('color', colors.GRAY1 + (255,))

        # set the background color
        self.set_background_color(*colors.GRAY0)

        # a player to have better sound playback
        self._player = pyglet.media.Player()

    #
    # pyglet event callbacks
    #

    def on_begin(self):
        # play the sound!
        if not self._player.playing:
            self._player.queue(self._snd_credits)
            self._player.play()

        # schedule a transition to the next state
        pyglet.clock.schedule_once(self._trans_splash, 2)

    def on_exit(self):
        # schedules cleanup
        pyglet.clock.unschedule(self._trans_splash)

    def _trans_splash(self, dt):
        # trigger a transition to the splash state
        self.transition_to('game_splash')

    def on_update(self):
        # Draw labels
        self._title_label.draw()
        self._presents_label.draw()
        super().on_update()  # draw things on parent
