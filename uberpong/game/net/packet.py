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

    [
        <proto_version>,
        <type_of_message>,
        <command>,
        <player_id>
    ]


Responses:
~~~~~~~~~~

Responses (regardless of source) must have as well a protocol version
specification. Moreover, these packets must have a status field, a reason
field (which is a nice string with a message explaining whatever status
there is in a response), following data all remaining keys are considered
variable data to be used by the receiving peer.
A general response looks like the following:

    [
        <proto_version>,
        <type_of_message>,
        (Depending on type of message)
        <status>,
        <reason>,
        <state>
        ...
        // variable data
        ...
    ]


Initial handshake and further communication:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First of all, in order for a client to have communication with a server,
it will need to acquire a valid player id. For this to happen,
a client must first handshake with a server, like so:

    (client) ~~>
        [
            1, # Protocol version
            30, # Type of message
            '+connect' # Command
        ]

    <~~ (server)
        [
            1, # Protocol version
            33, # Type of message
            20, # Status
            '25aee061a5f34977bf672d4ff59fdc36' # Player UUID
        ]

Once the server has acknowledged a client, the latter receives a valid
player id from which further requests can be made. From this point until
disconnection, the former will actively send the client periodic
update responses:

    (client) ~~>
        [
            1,
            30,
            '+move',
            '25aee061a5f34977bf672d4ff59fdc36'
        ]

    <~~ (server)
        [
            1, 31, # Protocol version and type of message
            20, 14, # Status, reason

            // variable data

            102, # state
            [
                [1, 1, 0, 14, -20], # player info
                [1, 24, 0, 23, 40]  # foe player info (could be null)
            ],
            [12, 4, 223, 140] # ball info
        ]
"""


class Packet:
    """Basic network packet implementation"""

    ############################################
    # Protocol version
    ############################################
    PROTO_VERSION = 1

    ############################################
    # Protocol indexes
    ############################################
    PI_VERSION = 0  # protocol version
    PI_TOM = 1  # type of message
    PI_STATUS = 2  # status
    PI_COMMAND = 2  # command

    ############################################
    # Types of message
    ############################################
    TOM_COMMAND = 30
    TOM_UPDATE = 31
    TOM_CONNECT = 32
    TOM_REPLY = 33

    def __init__(self, *,
                 data=None,
                 pi_playerid=None):
        """Constructor

        Args:
            data(dict): Initial data for this packet
        """

        # In order for the data to conserve its
        # random access, an initial None-filled
        # array is assigned as the initial data
        if data is None:
            data = [None for i in range(10)]
        self._data = data

        # Set protocol version
        self._data[self.PI_VERSION] = self.PROTO_VERSION

        # Protocol index for player id varies among
        # types of message
        self._pi_player_id = pi_playerid

    @property
    def data(self):
        """Raw data"""

        # Return a None-stripped copy of data
        d = self._data.copy()
        if len(d):
            while d[-1] is None:
                d.pop()
        return d

    @data.setter
    def data(self, value):
        """Set raw data"""
        self._data = value

    @property
    def tom(self):
        return self._data[self.PI_TOM]

    @tom.setter
    def tom(self, value):
        """Set raw data"""
        self._data[self.PI_TOM] = value

    @property
    def proto_version(self):
        """Get protocol version for this packet"""
        return self._data[self.PI_VERSION]

    @property
    def player_id(self):
        """Get player uuid"""
        if self._pi_player_id in range(len(self._data)):
            return self._data[self._pi_player_id]
        return None

    @player_id.setter
    def player_id(self, player_id):
        """Set player uuid"""
        self._data[self._pi_player_id] = player_id


class Request(Packet):
    """Request packet implementation"""

    ############################################
    # Commands included in the request protocol
    ############################################
    CMD_CONNECT = '+connect'
    CMD_DISCONNECT = '-connect'
    CMD_MV_UP = '+move'
    CMD_MV_DN = '-move'
    CMD_READY = '+ready'

    ############################################
    # Protocol indexes
    ############################################
    PI_PLAYER_ID = 3

    def __init__(self, *, command=None, **kwargs):
        super().__init__(pi_playerid=self.PI_PLAYER_ID, **kwargs)

        # Type of message
        self.tom = Packet.TOM_COMMAND

        # Set command
        if command is not None:
            self.command = command

    @property
    def command(self):
        """Get command"""
        if Packet.PI_COMMAND in range(len(self.data)):
            return self._data[Packet.PI_COMMAND]
        return None

    @command.setter
    def command(self, value):
        """Set command"""
        self._data[Packet.PI_COMMAND] = value


class Response(Packet):
    """Response packet implementation"""

    ############################################
    # Status codes
    ############################################
    STATUS_OK = 20
    STATUS_UNAUTHORIZED = 21

    ############################################
    # Reasons
    ############################################
    REASON_VERSION_NOT_SUPPORTED = 11
    REASON_CONN_REFUSED = 12
    REASON_CONN_GRANTED = 13
    REASON_ACCEPTED = 14
    REASON_UPDATE = 15

    ############################################
    # Protocol indexes
    ############################################
    PI_PLAYER_ID = 4
    PI_STATE = 4
    PI_REASON = 3
    PI_PLAYER_INFO = 5
    PI_BALL_INFO = 6

    def __init__(self, **kwargs):
        super().__init__(pi_playerid=self.PI_PLAYER_ID, **kwargs)

        # not necessarily
        self.tom = Packet.TOM_UPDATE

    @property
    def status(self):
        """Get status"""
        if Packet.PI_STATUS in range(len(self._data)):
            return self._data[Packet.PI_STATUS]
        return None

    @status.setter
    def status(self, value):
        """Set status"""
        self._data[Packet.PI_STATUS] = value

    @property
    def state(self):
        """Get state"""
        if self.PI_STATE in range(len(self._data)):
            return self._data[self.PI_STATE]
        return None

    @state.setter
    def state(self, value):
        """Set state"""
        self._data[self.PI_STATE] = value

    @property
    def reason(self):
        """Set reason"""
        if self.PI_REASON in range(len(self._data)):
            return self._data[self.PI_REASON]
        return None

    @reason.setter
    def reason(self, value):
        """Get reason"""
        self._data[self.PI_REASON] = value

    def set_player_info(self, *, name, number, score, position, velocity):
        """Set player information

        Kwargs:
            name(str): Player name
            number(int): Player number
            score(int): Player score
            position(int, int): Player's paddle position on the plane
            velocity(int, int): Player's paddle current velocity
        """

        if self._data[self.PI_PLAYER_INFO] is None:
            self._data[self.PI_PLAYER_INFO] = [None, None]

        if name == 'you':
            player_index = 0
        else:
            player_index = 1

        # In this part, player information is set linearly
        # in the array
        self._data[self.PI_PLAYER_INFO][player_index] = [number, score]
        self._data[self.PI_PLAYER_INFO][player_index].extend(list(position))
        self._data[self.PI_PLAYER_INFO][player_index].extend(list(velocity))

    def get_ball_info(self):
        try:
            ball_info = self._data[self.PI_BALL_INFO]
        except IndexError:
            return None

        return {
            'position': ball_info[:2],
            'velocity': ball_info[2:]
        }

    def set_ball_info(self, *, position, velocity):
        self._data[self.PI_BALL_INFO] = list(position)
        self._data[self.PI_BALL_INFO].extend(list(velocity))

    def get_player_info(self, *, name):
        """Get information regarding a specific player"""

        try:
            if name == 'you':
                player_info = self._data[self.PI_PLAYER_INFO][0]
            else:
                player_info = self._data[self.PI_PLAYER_INFO][1]
        except IndexError:
            return None

        return {
            'number': player_info[0],
            'score': player_info[1],
            'position': player_info[2:4],
            'velocity': player_info[4:]
        }
