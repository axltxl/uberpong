# -*- coding: utf-8 -*-

from engine.spot import spot_set, spot_get
from engine.net import Server
from engine.entity import Entity

from game.net.packet import PacketRequest, PacketResponse

MAX_PLAYERS = 2

class PlayerEntity(Entity):
    def __init__(self, uuid, **kwargs):
        super().__init__(uuid, a=32, b=64, **kwargs)

class BallEntity(Entity):
    pass

class BoardEntity(Entity):
    pass

class Scene(Server):
    def __init__(self, *, width, height, **kwargs):
        super().__init__(**kwargs)

        self._window_width = width
        self._window_height = height

        self._players = {}

        self._ent_mgr = spot_get('game_entity_manager')

        # Register entities
        self._ent_mgr.register_class('ent_player', PlayerEntity)

    def create_player(self):
        #
        player = self._ent_mgr.create_entity('ent_player')
        player.y = (self._window_height - player.b)//2

        #
        self._players[player.get_uuid()] = player

        #
        return player

    def on_data_received(self, data, host, port):
        #
        req = PacketRequest(data)
        res = PacketResponse()

        #
        if req.command is not None:
            if req.command == NetRequest.CMD_CONNECT:
                if len(self._players) < MAX_PLAYERS:
                    res.response = PacketResponse.RES_OK
                    res.player_id = self.create_player().get_uuid()

        #
        self.send(res.data, host, port)
