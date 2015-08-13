# -*- coding: utf-8 -*-

class PacketRequest:
    CMD_CONNECT = 'connect'
    def __init__(self, data={}):
        self._req = data

    @property
    def command(self):
        if 'cmd' in self._req:
            return self._req['cmd']
        return None

    @command.setter
    def command(self, value):
        self._req['cmd'] = value

    @property
    def data(self):
        return self._req


class PacketResponse:
    RES_OK = 'OK'
    RES_NOT_OK = 'NOT_OK'

    REASON_CONN_REFUSED = "conn_refused"

    def __init__(self, data={}):
        self._res = data

    @property
    def response(self):
        if 'res' in self._res:
            return self._res['res']
        return None

    @response.setter
    def response(self, value):
        self._res['res'] = value

    @property
    def reason(self):
        if 'reason' in self._res:
            return self._res['reason']
        return None

    @reason.setter
    def reason(self, value):
        self._res['reason'] = value

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
