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
        self._server = spot_get('game_server')
        self._client = spot_get('game_client')

    #
    # pyglet event callbacks
    #

    def on_begin(self):

        # #
        # # Get argv parsed options
        # #
        # options = spot_get('argv')
        #
        #
        # #
        # # Initialise server
        # #
        # if options['--host'] is None:
        #
        #     #
        #     server_addr = 'localhost'
        #
        #     #
        #     self._server = Scene(port=5000,
        #                         width=self._machine.window.width,
        #                         height=self._machine.window.height)
        #
        #     # Activate LZ4 compression on client
        #     if options['--lz4']:
        #         self._server.use_lz4 = True
        # else:
        #     server_addr = options["--host"]

        # #
        # # Create client
        # #
        # self._client = PlayerClient(
        #     ball_position=spot_get('ball_position_start'),
        #     address=server_addr,
        #     port=5000
        # )
        #
        # #
        # # Activate LZ4 compression on client
        # #
        # if options['--lz4']:
        #     self._client.use_lz4 = True

        #
        # Connect client to server
        # TODO: put this on 'game_load' state
        self._client.connect()

    def on_exit(self):
        pass
        # # Client disconnection
        # if self._client is not None:
        #     self._client.disconnect()
        #     self._client.close()
        #
        # # Scene server disconnection
        # if self._server is not None:
        #     self._server.close()


    def on_update(self):
        # Update client!
        if self._client is not None:
            # self._client.pump()
            self._client.draw()


    #######################################################
    # All input events are handled directly by the client
    #######################################################

    def on_key_press(self, symbol, modifiers):
        # Update data on client
        self._client.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        # Update data on client
        self._client.on_key_release(symbol, modifiers)
