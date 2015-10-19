# -*- coding: utf-8 -*-

"""
game.states.base
~~~~~~~~
Base state for this game sharing many
commong routines used throughout all states
of the game

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet
from pyglet.gl import *
from engine.state import State
from engine.spot import spot_set, spot_get

from ..net import Scene


class BaseState(State):
    """base state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # Get client and server
        self._server = spot_get('game_server')
        self._client = spot_get('game_client')

        #
        self._fade_out = False
        self._fade_in  = False
        self._fade_alpha = 0

        #
        self.sorcerer = spot_get('game_object').sorcerer

        #
        self.sorcerer.create_font('8-bit Operator+',
                file_name='8bitOperatorPlus-Regular.ttf')


    def create_label(self, text, *,
            font_size=15,
            x=None, y=None,
            bold=False,
            anchor_x='center', anchor_y='center'):

        if x is None:
            pos_x = self.window.width // 2
        else:
            pos_x = x

        if y is None:
            pos_y = self.window.height // 2
        else:
            pos_y = y

        return pyglet.text.Label(
            text, font_name='8-bit Operator+', font_size=font_size,
            x=pos_x, y=pos_y, bold=bold,
            anchor_x='center', anchor_y='center'
        )


    def set_background_color(self, red, green, blue, alpha=255):
        """ Set background color """
        pyglet.gl.glClearColor(red/255, green/255, blue/255, alpha/255)


    def _setup_fade(self, fade_func, total_time, alpha):
        self._fade_total_time = total_time/1000
        fade_interval = 1/60.0
        self._fade_step = int( 255 / (self._fade_total_time/fade_interval) )
        pyglet.clock.schedule_interval(fade_func, fade_interval)
        self._fade_alpha = alpha


    def transition_to(self, state_name, *, total_time=100):
        """ Trigger animated transition to state_name """
        self._fade_out = True
        self._trans_state_name = state_name
        self._setup_fade(self._fade_alpha_up, total_time, 0)


    def _fade_alpha_up(self, dt):
        self._fade_alpha += self._fade_step


    def _fade_alpha_down(self, dt):
        self._fade_alpha -= self._fade_step


    def on_exit(self):
        glDisable(GL_BLEND)
        pyglet.clock.unschedule(self._fade_alpha_up)
        pyglet.clock.unschedule(self._fade_alpha_down)
        self._fade_in = False
        self._fade_out = False


    def on_update(self):
        if self._fade_out or self._fade_in:
            glEnable(GL_BLEND)
            # draw the polygon depending on set alpha
            width = self.window.width
            height = self.window.height
            pyglet.graphics.draw(6, GL_TRIANGLES,
                    ('v2i',(0, height,
                            0, 0,
                            width, 0,

                            width, 0,
                            width, height,
                            0, height)
                    ),
                    # ('c3B',(10, 25, 0) * 6 )
                    ('c4B', (0, 0, 0, self._fade_alpha) * 6)
                )
            # Stop "fade" animation
            if self._fade_alpha >= 255:
                self.push(self._trans_state_name)


    @property
    def server(self):
        return self._server


    @property
    def client(self):
        return self._client


