# -*- coding: utf-8 -*-

class Packet:

    # Protocol version
    PROTO_VERSION = 1


    def __init__(self, data=None):
        if data is None:
            data = {}
        self._data = data

        self._data['version'] = self.PROTO_VERSION

    @property
    def data(self):
        return self._data

    @property
    def proto_version(self):
        return self._data['version']

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
    CMD_CONNECT = '+connect'
    CMD_DISCONNECT = '-connect'

    CMD_MV_UP = '+move'
    CMD_MV_DN = '-move'

    @property
    def command(self):
        if 'cmd' in self.data:
            return self.data['cmd']
        return None

    @command.setter
    def command(self, value):
        self.data['cmd'] = value


class PacketResponse(Packet):

    #
    # Status codes
    #
    STATUS_OK = 'OK'
    STATUS_UNAUTHORIZED = 'Unauthorized'

    #
    # Reasons
    #
    REASON_VERSION_NOT_SUPPORTED = 'Version Not Supported'
    REASON_CONN_REFUSED = "Connection Refused"
    REASON_CONN_GRANTED = 'Connection Granted'
    REASON_ACCEPTED = 'Accepted'

    @property
    def status(self):
        if 'status' in self.data:
            return self.data['status']
        return None

    @status.setter
    def status(self, value):
        self.data['status'] = value

    @property
    def reason(self):
        if 'reason' in self.data:
            return self.data['reason']
        return None

    @reason.setter
    def reason(self, value):
        self.data['reason'] = value
