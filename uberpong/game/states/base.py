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
import pyglet.gl

from uberpong.engine.state import State
from uberpong.engine.spot import spot_get

from .. import utils


class BaseState(State):
    """base state"""

    def __init__(self, *, machine, fade_in=False):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # Get client and server
        self._server = spot_get('game_server')
        self._client = spot_get('game_client')

        # initial values for fade animation flags and alpha
        self._fade_out = False
        self._fade_in = False
        self._fade_alpha = 0

        # get the sorcerer to use resources
        self.sorcerer = spot_get('game_object').sorcerer

        # create the base fonts used throughout the entire game
        self.sorcerer.create_font(
            utils.FONT_SECONDARY,
            file_name='8bitOperatorPlus8-Regular.ttf'
        )
        self.sorcerer.create_font(
            utils.FONT_PRIMARY,
            file_name='8bitOperatorPlus-Regular.ttf'
        )

        # fade attributes
        self._fade_step = None
        self._fade_total_time = None
        self._trans_state_name = None

        # TODO: give more flexibility about this
        if fade_in:
            self._sched_fadein(100)

    def create_label(self, text, **kwargs):
        """ Create a pyglet label easily

        Args:
            text(str): Initial text for this resource

        Kwargs:
            kwargs(dict, optional): optional keyword arguments
        """

        return utils.create_label(text, window=self.window, **kwargs)

    def set_background_color(self, red, green, blue, alpha=255):
        """ Set background color

        Args:
            red(int): amount of red in this color
            green(int): amount of green in this color
            blue(int): amount of blue in this color
            alpha(int): amount of alpha in this color
        """
        pyglet.gl.glClearColor(red/255, green/255, blue/255, alpha/255)

    def _setup_fade(self, total_time, alpha):
        """Set up fade animation and schedule it"""

        # total fade animation time in seconds
        self._fade_total_time = total_time/1000

        # updates to animation are going to be made at 60 fps
        fade_interval = 1/60.0

        # the amount of alpha applied to the fade polygon is relative to both
        # the total time of the animation and its interval time
        self._fade_step = int(255 / (self._fade_total_time/fade_interval))

        # actually schedule the animation under the set interval
        pyglet.clock.schedule_interval(self._fade_alpha_step, fade_interval)

        # set initial alpha
        self._fade_alpha = alpha

    def _sched_fadein(self, total_time):
        self._fade_in = True
        self._sched_fade_anim(total_time, 255)

    def _sched_fadeout(self, total_time, state_name):
        self._fade_out = True
        self._trans_state_name = state_name
        self._sched_fade_anim(total_time, 0)

    def _sched_fade_anim(self, total_time, initial_alpha):
        self._setup_fade(total_time, initial_alpha)

    def transition_to(self, state_name, *, total_time=100):
        """ Trigger animated transition to state_name

        Args:
            state_name(str): key name of the state to push after fade in/out
        Kwargs:
            total_time(int, optional): animation total time in milliseconds
        """

        self._sched_fadeout(total_time, state_name)

    def _fade_alpha_step(self, dt):
        if self._fade_out:
            self._fade_alpha += self._fade_step
            # make sure alpha reaches no more than its top value
            if self._fade_alpha > 255:
                self._fade_alpha = 255
        if self._fade_in:
            self._fade_alpha -= self._fade_step
            # make sure alpha reaches no more than its bottom value
            if self._fade_alpha < 0:
                self._fade_alpha = 0

    def _fade_cleanup(self):
        """Clean up everyhing before exiting"""

        pyglet.clock.unschedule(self._fade_alpha_step)
        self._fade_in = False
        self._fade_out = False

    def on_update(self):
        if self._fade_out or self._fade_in:
            pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
            # draw the polygon depending on set alpha
            width = self.window.width
            height = self.window.height
            pyglet.graphics.draw(
                6, pyglet.gl.GL_TRIANGLES,
                ('v2i', (0, height,
                         0, 0,
                         width, 0,

                         width, 0,
                         width, height,
                         0, height)),
                ('c4B', (0, 0, 0, self._fade_alpha) * 6)
            )
            pyglet.gl.glDisable(pyglet.gl.GL_BLEND)

            # Stop "fade" animation
            if self._fade_out:
                if self._fade_alpha == 255:
                    self._fade_cleanup()
                    self.push(self._trans_state_name)

            if self._fade_in:
                if not self._fade_alpha:
                    self._fade_cleanup()

    @property
    def server(self):
        """Get the running server"""
        return self._server

    @property
    def client(self):
        """Get the running client"""
        return self._client
