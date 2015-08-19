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

from game.net.player import PlayerClient
from game.net.scene import Scene

class GameState(State):
    """Game start state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # TODO: document this!
        self._scene = None
        self._player = None

    #
    # pyglet event callbacks
    #

    def on_begin(self):

        #
        # Get argv parsed options
        #
        options = spot_get('argv')


        #
        # Initialise server
        #
        if options['--host'] is None:

            #
            server_addr = 'localhost'

            #
            self._scene = Scene(port=5000,
                                width=self._machine.window.width,
                                height=self._machine.window.height)

            # Activate LZ4 compression on client
            if options['--lz4']:
                self._scene.use_lz4 = True
        else:
            server_addr = options["--host"]

        #
        # Create client
        #
        self._player = PlayerClient(
            ball_position=spot_get('ball_position_start'),
            address=server_addr,
            port=5000
        )

        #
        # Activate LZ4 compression on client
        #
        if options['--lz4']:
            self._player.use_lz4 = True

        #
        # Connect client to server
        #
        self._player.connect()

    def on_exit(self):
        # Client disconnection
        if self._player is not None:
            self._player.disconnect()
            self._player.close()

        # Scene server disconnection
        if self._scene is not None:
            self._scene.close()


    def on_update(self):
        # Update client!
        if self._player is not None:
            self._player.pump()
            self._player.draw()


    #######################################################
    # All input events are handled directly by the client
    #######################################################

    def on_key_press(self, symbol, modifiers):
        # Update data on client
        self._player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        # Update data on client
        self._player.on_key_release(symbol, modifiers)
