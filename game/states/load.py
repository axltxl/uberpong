# -*- coding: utf-8 -*-

"""
game.states.load
~~~~~~~~
Round state

Purpose:
* The client tries to connect to a server
* A nice "Connecting to server..." text is drawn here

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

from engine.state import State
from engine.spot import spot_set, spot_get


class LoadState(State):
    """Game start state"""

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

        #
        self._push_schedule = False

        # Connect label
        self._conn_label = pyglet.text.Label(
            "Connecting to server...", font_name='8-bit Operator+', font_size=32,
            x=machine.window.width//2, y=machine.window.height//2,
            anchor_x='center', anchor_y='center'
        )

        # Server label
        self._server_label = pyglet.text.Label(
            "@ pong://{}:{}".format(self._client.server_address, self._client.server_port),
            font_name='8-bit Operator+', font_size=24,
            x=machine.window.width//2, y=machine.window.height//2 - 40,
            anchor_x='center', anchor_y='center'
        )

        # Connected label
        self._connected_label = pyglet.text.Label(
            "CONNECTED!", font_name='8-bit Operator+', font_size=32,
            x=machine.window.width//2, y=machine.window.height//2,
            anchor_x='center', anchor_y='center'
        )



    #
    # pyglet event callbacks
    #

    def _get_going(self, dt):
        self.push('game_wait') #  temp
        # TODO: implement this when the time comes
        # if self._server is not None:
        #     self.push('game_waitforplayer')
        # else:
        #     self.push('game_begin')

    def _attempt_connection(self, dt):
        if not self._client.connected:
            self._client.connect()

    def on_begin(self):
        #
        # Connect client to server
        #
        pyglet.clock.schedule_interval(self._attempt_connection, 1)

    def on_update(self):

        #
        # Check whether the client has connected to the server
        #
        if self._client.connected:
            if not self._push_schedule:
                # Schedule a new state onto the stack after the sound has been played
                pyglet.clock.schedule_once(self._get_going, 3)

                #
                pyglet.clock.unschedule(self._attempt_connection)

                #
                self._push_schedule = True

            #
            self._connected_label.draw()

        else:
            # Draw labels
            self._conn_label.draw()
            self._server_label.draw()
