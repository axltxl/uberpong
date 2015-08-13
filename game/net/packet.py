# -*- coding: utf-8 -*-

class PacketRequest(object):
    CMD_CONNECT = 'connect'
    def __init__(self, data):
        self._data = data

    @property
    def command(self):
        if 'cmd' in self._data:
            return self._data['cmd']
        return None

    @command.setter
    def command(self, value):
        self._data['cmd'] = value

class PacketResponse(object):
    RES_OK = 'OK'
    RES_NOT_OK = 'NOT_OK'

    def __init__(self, *, response=RES_NOT_OK):
        self._res = {"res":response}

    @property
    def response(self):
        return self._res['res']

    @response.setter
    def response(self, value):
        self._res['res'] = value

    @property
    def player_id(self):
        if 'player_id' in self._res:
            return self._res['player_id']
        return None

    @player_id.setter
    def player_id(self, id):
        self._res['player_id'] = id

    @property
    def data(self):
        return self._res
