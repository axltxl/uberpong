# -*- coding: utf-8 -*-

from engine.spot import spot_set, spot_get
from engine.net import Server
from engine.entity import Entity

from game.net.packet import PacketRequest, PacketResponse

class PlayerEntity(Entity):
    def __init__(self, uuid, **kwargs):
        super().__init__(uuid, size=(32, 64), **kwargs)

class BallEntity(Entity):
    pass

class BoardEntity(Entity):
    pass

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

        #
        return player

    def on_data_received(self, data, host, port):
        #
        req = PacketRequest(data)

        res = PacketResponse()
        res.response = PacketResponse.RES_NOT_OK

        #
        if req.command is not None:
            if req.command == PacketRequest.CMD_CONNECT:
                if len(self._players) < self.MAX_PLAYERS:
                    res.response = PacketResponse.RES_OK
                    res.player_id = self.create_player(host, port).get_uuid()
                else:
                    res.reason = PacketResponse.REASON_CONN_REFUSED

        #
        self.send(res.data, host, port)
