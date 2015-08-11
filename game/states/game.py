# -*- coding: utf-8 -*-

"""
game.states.game
~~~~~~~~
Game state

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet
from engine.state import State
from engine.spot import spot_set, spot_get

import PodSixNet.Channel
import PodSixNet.Server

class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data

class Server(PodSixNet.Server.Server):

    channelClass = ClientChannel

    def Connected(self, channel, addr):
        print 'new connection:', channel


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
        self._server = Server()

    #
    # pyglet event callbacks
    #

    def on_begin(self):
        # Initialise server
        # Connect client to server
        pass

    def on_update(self):
        # Update client with data from server (unless the client is event-driven)
        # Perform actions inside the client based on new data (client.update or something)
        # Send data from client to server (client.sent_data or something)
        # Render all the things on client! (client.draw)
        # Update server!
        self._server.Pump()

    #######################################################
    # All input events are handled directly by the client
    #######################################################

    def on_key_press(self, sym, mod):
        # Update data on client
        # maybe send packets to the server as the player hits buttons
        pass
