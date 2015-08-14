# -*- coding: utf-8 -*-

from engine.spot import spot_set, spot_get
from engine.net import Server

from game.net.packet import Packet, PacketRequest, PacketResponse
from game.entities.player import PlayerEntity


class Scene(Server):
    MAX_PLAYERS = 2

    def __init__(self, *, width, height, **kwargs):
        super().__init__(**kwargs)

        self._window_width = width
        self._window_height = height

        self._players = {}

        self._ent_mgr = spot_get('game_entity_manager')

        # Register entities
        self._ent_mgr.register_class('ent_player', PlayerEntity)

    def create_player(self, host, port):
        #
        player = self._ent_mgr.create_entity('ent_player')
        #player.move_abs(0, (self._window_height - player.height)//2)
        player.move_abs(0, 0)

        #
        self._players[player.uuid] = {
            "entity": player,
            "host": host,
            "port": port
        }

        # Return the thing
        return player

    def on_data_received(self, data, host, port):
        #
        # Get a nice PacketRequest from raw data
        #
        request = PacketRequest(data)

        #
        # By default, the server will not be OK with the incoming request
        #
        response = PacketResponse()
        response.status = PacketResponse.STATUS_UNAUTHORIZED
        response.reason = PacketResponse.REASON_CONN_REFUSED

        # TODO: Check for protocol version
        # if request.proto_version != Packet.PROTO_VERSION:
        #     # Send the packet to the client
        #     response.reason.REASON_VERSION_NOT_SUPPORTED
        #     self.send(response.data, host, port)
        #     return

        #######################################
        # Check packet
        #######################################
        if request.command is not None:
            if request.player_id is None:
                if request.command == PacketRequest.CMD_CONNECT:
                    if len(self._players) < self.MAX_PLAYERS:
                        response.status = PacketResponse.STATUS_OK
                        response.reason = PacketResponse.REASON_CONN_GRANTED
                        response.player_id = self.create_player(host, port).uuid

            elif request.player_id in self._players:
                # packet is valid and going to be processed
                print(request.data)

                #
                player = self._players[request.player_id]['entity']
                command = request.command

                # update command
                # +move command
                if command == PacketRequest.CMD_MV_UP:
                    player.move_rel(dy=1)
                # -move command
                elif command == PacketRequest.CMD_MV_DN:
                    player.move_rel(dy=-1)

                print(player.coordinates)

                # Set the answer as accepted
                response.status = PacketResponse.STATUS_OK
                response.reason = PacketResponse.REASON_ACCEPTED

        # Send the packet to the client
        self.send(response.data, host, port)
