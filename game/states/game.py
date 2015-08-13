# -*- coding: utf-8 -*-

"""
game.states.game
~~~~~~~~
Game state

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet
import socket

from engine.state import State
from engine.spot import spot_set, spot_get

from game.player import PlayerClient
from game.board import Scene

class GameState(State):
    """Game start state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # Create a single client and server
        self._scene = Scene(port=5000,
                            width=machine.window.width,
                            height=machine.window.height)
        self._player = PlayerClient(port=5000)


    #
    # pyglet event callbacks
    #

    def on_begin(self):
        # Initialise server
        # Connect client to server
        pass

    def on_exit(self):
        self._scene.close()
        self._player.close()

    def on_update(self):
        # Update client with data from server (unless the client is event-driven)
        # Perform actions inside the client based on new data (client.update or something)
        # Send data from client to server (client.sent_data or something)
        # Render all the things on client! (client.draw)

        # Update client!
        self._player.pump()

        # Update server!
        self._scene.pump()

    #######################################################
    # All input events are handled directly by the client
    #######################################################

    def on_key_press(self, symbol, modifiers):
        # Update data on client
        self._player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        # Update data on client
        self._player.on_key_release(symbol, modifiers)
