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


from ..net import Scene
from .base import BaseState


class BeginState(BaseState):
    """Game begin state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # Server label
        self._wait_label = self.create_label(
            '',
            font_size=20,
            x=machine.window.width//2, y=16,
            anchor_y='baseline'
        )

    #
    # pyglet event callbacks
    #

    def on_begin(self):
        self._wait_label.text = "Press any key when you are READY ..."
        if self._server is not None:
            self._server.reset_players()
            self._server.reset_ball()

    def on_update(self):
        """Draw all the things!"""

        self.client.tick()
        self.client.draw_board()
        self.client.draw_ball()
        self.client.draw_paddles()
        self._wait_label.draw()

        # Check for a state change, at anytime is expected
        # from the server to change to "playing" state
        if self.client.server_state == Scene.ST_PLAYING:
            self.push('game_round')

    #######################################################
    # All input events are handled directly by the client
    #######################################################

    def on_key_press(self, symbol, modifiers):

        # Update the text
        self._wait_label.text = "Ready!"

        # Update data on client
        self.client.on_key_press(symbol, modifiers)
