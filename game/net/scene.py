# -*- coding: utf-8 -*-

from engine.spot import spot_set, spot_get
from engine.net import Server

from game.net.packet import PacketRequest, PacketResponse
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
        player.move_abs(0, (self._window_height - player.height)//2)

        #
        self._players[player.get_uuid()] = {
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
        response.response = PacketResponse.RES_NOT_OK
        response.reason = PacketResponse.REASON_CONN_REFUSED

        #
        # Check packet
        #
        if request.command is not None:
            if request.player_id is None:
                if request.command == PacketRequest.CMD_CONNECT:
                    if len(self._players) < self.MAX_PLAYERS:
                        response.response = PacketResponse.RES_OK
                        response.player_id = self.create_player(host, port).get_uuid()

            elif request.player_id in self._players:
                # packet is valid and going to be processed
                # update command
                # +move command
                # -move command
                pass

        # Send the packet to the client
        self.send(response.data, host, port)
