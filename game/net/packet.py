# -*- coding: utf-8 -*-

"""
game.net.packet
~~~~~~~~
Network packet abstractions for easier handling

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

"""
JSON-over-UDP Network protocol:
~~~~~~~~~~~~~~~~~~~~~~~~~~
This game's network protocol is a connectionless exchange of serialized
JSON strings, which are decoded and loaded as dictionaries on peers.


Requests:
~~~~~~~~~

A generic request is generally cooked with at least
a protocol version field, a command field and a player id, like so:

    {
        'version': <proto_version>,
        'cmd': <command>,
        'player_id': <id>
    }


Responses:
~~~~~~~~~~

Responses (regardless of source) must have as well a protocol version
specification. Moreover, these packets must have a status field, a reason
field (which is a nice string with a message explaining whatever status
there is in a response), following data all remaining keys are considered
variable data to be used by the receiving peer.
A general response looks like the following:

    {
        'version': <proto_version>,
        'status': <status_code>,
        'reason': <reason_string>,
        <variable data ...>
    }


Initial handshake and further communication:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First of all, in order for a client to have communication with a server,
it will need to acquire a valid player id. For this to happen,
a client must first handshake with a server, like so:

    client ~~>
        {
            'version': 1,
            'cmd': '+connect'
        }

    <~~ server
        {
            'version': 1,
            'status': 'OK',
            'reason': 'Connection Granted',
            'player_id': '25aee061a5f34977bf672d4ff59fdc36'
        }

Once the server has acknowledged a client, the latter receives a valid
player id from which further requests can be made:

    client ~~>
        {
            'version': 1,
            'cmd': '+move',
            'player_id': '25aee061a5f34977bf672d4ff59fdc36'
        }

    <~~ server
        {
            'version': 1,
            'status': 'OK',
            'state': 'PLAYING',
            'reason': 'Accepted',
            'players': {
                'you': {
                    'score': 1,
                    'position': {
                        'y': 1, 'x': 0
                    }
                }
                'foe': {
                    'score': 1,
                    'position': {
                        'y': 24, 'x': 0
                    }
                }
            },
            'ball': {
                'x': 12, 'y': 4
            }
        }

    client ~~>
        {
            'version': 1,
            'cmd': '+move',
            'player_id': '25aee061a5f34977bf672d4ff59fdc36'
        }

    <~~ server
        {
            'version': 1,
            'status': 'OK',
            'state': 'PLAYING',
            'reason': 'Accepted',
            'players': {
                'you': {
                    'score': 1,
                    'position': {
                        'y': 5, 'x': 0
                    }
                }
                'foe': {
                    'score': 1,
                    'position': {
                        'y': 3, 'x': 0
                    }
                }
            },
            'ball': {
                'x': 0, 'y': 27
            }
        }

"""


class Packet:
    """Basic network packet implementation"""

    # Protocol version
    PROTO_VERSION = 1

    def __init__(self, data=None):
        """Constructor

        Args:
            data(dict): Initial data for this packet
        """
        if data is None:
            data = {}
        self._data = data

        self._data['version'] = self.PROTO_VERSION

    @property
    def data(self):
        """Raw data"""
        return self._data

    @data.setter
    def data(self, value):
        """Set raw data"""
        self._data = value

    @property
    def proto_version(self):
        """Get protocol version for this packet"""
        return self._data['version']

    @property
    def player_id(self):
        """Get player uuid"""
        if 'player_id' in self.data:
            return self.data['player_id']
        return None

    @player_id.setter
    def player_id(self, id):
        """Set player uuid"""
        self.data['player_id'] = id


class Request(Packet):
    """Request packet implementation"""

    ############################################
    # Commands included in the request protocol
    ############################################
    CMD_CONNECT = '+connect'
    CMD_DISCONNECT = '-connect'
    CMD_MV_UP = '+move'
    CMD_MV_DN = '-move'

    @property
    def command(self):
        """Get command"""
        if 'cmd' in self.data:
            return self.data['cmd']
        return None

    @command.setter
    def command(self, value):
        """Set command"""
        self.data['cmd'] = value


class Response(Packet):
    """Response packet implementation"""

    ############################################
    # Status codes
    ############################################
    STATUS_OK = 'OK'
    STATUS_UNAUTHORIZED = 'Unauthorized'

    ############################################
    # Reasons
    ############################################
    REASON_VERSION_NOT_SUPPORTED = 'Version Not Supported'
    REASON_CONN_REFUSED = "Connection Refused"
    REASON_CONN_GRANTED = 'Connection Granted'
    REASON_ACCEPTED = 'Accepted'

    @property
    def status(self):
        """Get status"""
        if 'status' in self.data:
            return self.data['status']
        return None

    @status.setter
    def status(self, value):
        """Set status"""
        self.data['status'] = value

    @property
    def reason(self):
        """Set reason"""
        if 'reason' in self.data:
            return self.data['reason']
        return None

    @reason.setter
    def reason(self, value):
        """Get reason"""
        self.data['reason'] = value
