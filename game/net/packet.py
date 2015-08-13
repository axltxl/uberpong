# -*- coding: utf-8 -*-

class Packet:
    def __init__(self, data=None):
        if data is None:
            data = {}
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def player_id(self):
        if 'player_id' in self.data:
            return self.data['player_id']
        return None

    @player_id.setter
    def player_id(self, id):
        self.data['player_id'] = id


class PacketRequest(Packet):
    CMD_CONNECT = 'connect'

    @property
    def command(self):
        if 'cmd' in self.data:
            return self.data['cmd']
        return None

    @command.setter
    def command(self, value):
        self.data['cmd'] = value


class PacketResponse(Packet):
    RES_OK = 'OK'
    RES_NOT_OK = 'NOT_OK'

    REASON_CONN_REFUSED = "conn_refused"

    @property
    def response(self):
        if 'res' in self.data:
            return self.data['res']
        return None

    @response.setter
    def response(self, value):
        self.data['res'] = value

    @property
    def reason(self):
        if 'reason' in self.data:
            return self.data['reason']
        return None

    @reason.setter
    def reason(self, value):
        self.data['reason'] = value
