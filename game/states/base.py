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


    def set_background_color(self, red, green, blue, alpha=1):
        """ Set background color """
        pyglet.gl.glClearColor(red, green, blue, alpha)


    @property
    def server(self):
        return self._server


    @property
    def client(self):
        return self._client


