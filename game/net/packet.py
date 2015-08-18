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

    (client) ~~>
        {
            'version': 1,
            'cmd': '+connect'
        }

    <~~ (server)
        {
            'version': 1,
            'status': 'OK',
            'reason': 'Connection Granted',
            'player_id': '25aee061a5f34977bf672d4ff59fdc36'
        }

Once the server has acknowledged a client, the latter receives a valid
player id from which further requests can be made. From this point until
disconnection, the former will actively send the client periodic
update responses:

    (client) ~~>
        {
            'version': 1,
            'cmd': '+move',
            'player_id': '25aee061a5f34977bf672d4ff59fdc36'
        }

    (client) ~~>
        {
            'version': 1,
            'cmd': '+move',
            'player_id': '25aee061a5f34977bf672d4ff59fdc36'
        }

    (client) ~~>
        {
            'version': 1,
            'cmd': '-move',
            'player_id': '25aee061a5f34977bf672d4ff59fdc36'
        }

    <~~ (server)
        {
            'version': 1,
            'status': 'OK',
            'state': 'PLAYING',
            'reason': 'Update',
            'players': {
                'you': {
                    'score': 1,
                    'position': {
                        'y': 1, 'x': 0
                    },
                    'velocity': {
                        'y': 14, 'x': -20
                    }
                }
                'foe': {
                    'score': 1,
                    'position': {
                        'y': 24, 'x': 0
                    },
                    'velocity': {
                        'y': 23, 'x': 40
                    }
                }
            },
            'ball': {
                'position': {
                    'x': 12, 'y': 4
                },
                'velocity': {
                    'y': 223, 'x': 140
                }
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

        # Set protocol version
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
    def player_id(self, player_id):
        """Set player uuid"""
        self.data['player_id'] = player_id


    def set_player_info(self, *, name, score, position, velocity):
        """Set player information

        Kwargs:
            name(str): Player name
            score(int): Player score
            position(int, int): Player's paddle position on the plane
            velocity(int, int): Player's paddle current velocity
        """

        if not 'players' in self.data:
            self.data['players'] = {}

        self.data['players'][name] ={
            'score': score,
            'position': {
                'x': position[0],
                'y': position[1]
            },
            'velocity': {
                'x': velocity[0],
                'y': velocity[1]
            }
        }

    def set_ball_info(self, *, position, velocity):
        self.data['ball'] = {
            'position': {'x': position[0], 'y': position[1]},
            'velocity': {'x': velocity[0], 'y': velocity[1]}
        }


    def get_player_info(self, *, name):
        """Get information regarding a specific player"""

        if 'players' in self.data:
            if name in self.data['players']:
                return self.data['players'][name]
        return None


class Request(Packet):
    """Request packet implementation"""

    ############################################
    # Commands included in the request protocol
    ############################################
    CMD_CONNECT = '+connect'
    CMD_DISCONNECT = '-connect'
    CMD_MV_UP = '+move'
    CMD_MV_DN = '-move'

    def __init__(self, data=None, *, command=None, **kwargs):
        super().__init__(data, **kwargs)

        if command is not None:
            self.command = command


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
    REASON_UPDATE = 'Update'


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
