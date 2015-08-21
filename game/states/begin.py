# -*- coding: utf-8 -*-

"""
game.states.begin
~~~~~~~~
Game begin state

Purpose:
* Set up board
* Reset score count
* Reset players to their original position
* Wait for players to be ready

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

from engine.state import State
from engine.spot import spot_set, spot_get

from ..net import Scene


class BeginState(State):
    """Game begin state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # Get client a server
        self._server = spot_get('game_server')
        self._client = spot_get('game_client')

        # Server label
        self._wait_label = pyglet.text.Label(
            "Press any key when you are READY ...",
            font_name='8-bit Operator+', font_size=20,
            x=machine.window.width//2, y=48,
            anchor_x='center', anchor_y='center'
        )

    #
    # pyglet event callbacks
    #


    def on_begin(self):
        if self._server is not None:
            self._server.reset_players()
            self._server.reset_ball()

        #self._client.reset_paddles()
        #self._client.reset_ball()


    def on_update(self):
        self._wait_label.draw()
        self._client.tick()
        self._client.draw_ball()
        self._client.draw_paddles()

        if self._client.server_state == Scene.ST_PLAYING:
            self.push('game_round')

    #######################################################
    # All input events are handled directly by the client
    #######################################################

    def on_key_press(self, symbol, modifiers):
        # Update data on client
        self._client.on_key_press(symbol, modifiers)
