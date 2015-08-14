# -*- coding: utf-8 -*-

"""
game.net.scene
~~~~~~~~
Client implementation for a player

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

from engine.spot import spot_set, spot_get
from engine.net import Server

from game.net.packet import Packet, Request, Response
from game.entities.player import PlayerEntity


class Scene(Server):
    """
    Scene server implementation

    This bad boy handles the game per se, by keeping and
    controlling entities and pumping responses to clients so
    they can do their rendering.
    """

    # Maximum number of players (clients) allowed to join the game
    MAX_PLAYERS = 2

    def __init__(self, *, width, height, **kwargs):
        """Constructor

        Args:
            width(int): width of the scene in pixels
            height(int): height of the scene in pixels
        """
        super().__init__(**kwargs)

        # Set scene dimensions
        self._window_width = width
        self._window_height = height

        # Players (and their related information) will be held in here
        self._players = {}

        # Get the entity manager
        self._ent_mgr = spot_get('game_entity_manager')

        # Register entities
        self._ent_mgr.register_class('ent_player', PlayerEntity)

    def create_player(self, host, port):
        """Create a PlayerEntity for a client

        Args:
            host(str): client address
            port(int): client port
        """

        # New PlayerEntity for a client
        player = self._ent_mgr.create_entity('ent_player')

        # Set initial position for this player
        #player.move_abs(0, (self._window_height - player.height)//2)
        player.move_abs(0, 0)

        # Save information for this new player
        self._players[player.uuid] = {
            "entity": player,
            "host": host,
            "port": port
        }

        # Return the thing
        return player

    def on_data_received(self, data, host, port):
        """Pump network requests from clients

        Args:
            data(dict): incoming raw data
            host(str): client address
            port(int): client port
        """
        #
        # Get a nice Request from raw data
        #
        request = Request(data)

        #
        # By default, the server will not be OK with the incoming request
        #
        response = Response()
        response.status = Response.STATUS_UNAUTHORIZED
        response.reason = Response.REASON_CONN_REFUSED

        # TODO: Check for protocol version
        # if request.proto_version != Packet.PROTO_VERSION:
        #     # Send the packet to the client
        #     response.reason.REASON_VERSION_NOT_SUPPORTED
        #     self.send(response.data, host, port)
        #     return

        #######################################
        # The actual pump
        #######################################
        if request.command is not None:
            if request.player_id is None:
                #
                # Client is trying to establish a connection
                #
                if request.command == Request.CMD_CONNECT:
                    if len(self._players) < self.MAX_PLAYERS:
                        response.status = Response.STATUS_OK
                        response.reason = Response.REASON_CONN_GRANTED
                        response.player_id = self.create_player(host, port).uuid

            elif request.player_id in self._players:
                #
                # Request is valid and going to be processed
                #
                print(request.data)

                #
                player = self._players[request.player_id]['entity']
                command = request.command

                # update command

                # +move command
                if command == Request.CMD_MV_UP:
                    player.move_rel(dy=1)

                # -move command
                elif command == Request.CMD_MV_DN:
                    player.move_rel(dy=-1)

                # TEMP
                print(player.coordinates)

                # Set the answer as accepted
                response.status = Response.STATUS_OK
                response.reason = Response.REASON_ACCEPTED

        # Send the packet to the client
        self.send(response.data, host, port)
