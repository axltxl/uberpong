# -*- coding: utf-8 -*-

"""
game.states.score
~~~~~~~~
A player has scored

Purpose:
* Increase count on winning player
* Check whether one of the players has reached the max score

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet
from .base import BaseState
from uberpong.engine.spot import spot_set, spot_get
from .. import colors
from ..net import Scene


class ScoreState(BaseState):
    """Game score state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # score sound
        self._snd_score = self.sorcerer.create_sound(
                'snd_score',
                file_name='Jingle_Achievement_00.wav'
        )

        # toggle flags
        self._show_scores = True

        # a player to have better sound playback
        self._player = pyglet.media.Player()

    #
    # pyglet event callbacks
    #

    def _toggle_show_scores(self, dt):
        self._show_scores ^= True


    def on_begin(self):
        pyglet.clock.schedule_interval(self._toggle_show_scores, 0.1)
        self.set_background_color(*colors.CRIMSON)

        #play the sound!
        if not self._player.playing:
           self._player.queue(self._snd_score)
           self._player.play()


    def on_exit(self):
        pyglet.clock.unschedule(self._toggle_show_scores)

    def on_update(self):
        # Draw all the things but the ball in the client!
        if self._show_scores:
            self.client.draw_scores()
        self.client.draw_paddles()

        # Switch to previous state
        if self.client.server_state == Scene.ST_PLAYING:
            self.pop()
        elif self.client.server_state == Scene.ST_GAME_SET:
            self.push('game_set')
