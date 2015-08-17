# -*- coding: utf-8 -*-

"""
game.net.scene
~~~~~~~~
Client implementation for a player

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

from engine.spot import spot_set, spot_get
from engine.net import Server
from engine.entity import EntityManager

from game.net.packet import Packet, Request, Response
from game.entities.player import PlayerPaddle
from game.entities.board import Board
from game.entities.ball import Ball


class Scene(Server):
    """
    Scene server implementation

    This bad boy handles the game per se, by keeping and
    controlling entities and pumping responses to clients so
    they can do their rendering.
    """

    # Maximum number of players (clients) allowed to join the game
    MAX_PLAYERS = 2

    def __init__(self, *, width, height, **kwargs):
        """Constructor

        Kwargs:
            width(int): width of the scene in pixels
            height(int): height of the scene in pixels
        """
        super().__init__(**kwargs)

        # Set scene dimensions
        self._window_width = width
        self._window_height = height

        # Set up the actual EntityManager
        self._ent_mgr = EntityManager()

        # set gravity
        self._ent_mgr.gravity = spot_get('sv_gravity')

        # Board
        self._board = Board(width, height, self._ent_mgr)

        # Players (and their related information) will be held in here
        self._players = {}

        # Register entities
        self._ent_mgr.register_class('ent_player', PlayerPaddle)
        self._ent_mgr.register_class('ent_ball', Ball)

        # Time scale (for in-server physics)
        self._timescale = spot_get('timescale')

        # Paddle impulse and top speed
        self._paddle_impulse = spot_get('sv_paddle_impulse')
        self._paddle_max_velocity = spot_get('sv_paddle_max_velocity')

        #
        self.create_ball()


    def create_ball(self):
        """Create a ball to play"""
        # New PlayerPaddle for a client
        self._ball = self._ent_mgr.create_entity('ent_ball')

        # Set initial position for this ball
        self._ball.position = spot_get('ball_position_start')

        #FIXME: do something
        self._ball.apply_impulse((-250, 0))


    def create_player(self, host, port):
        """Create a PlayerPaddle for a client

        Args:
            host(str): client address
            port(int): client port
        """

        # New PlayerPaddle for a client
        player = self._ent_mgr.create_entity('ent_player')

        # Set initial position for this player
        player.position = spot_get('paddle_position_start')


        # Save information for this new player
        self._players[player.uuid] = {
            "entity": player,
            "host": host,
            "port": port,
            "number": len(self._players),
            "foe": None
        }

        # Return the thing
        return player

    def update_players(self):
        for uuid, player_info in self._players.items():
            foes = [p['entity'].uuid for p in self._players.values() if p['entity'].uuid != uuid]
            if len(foes):
                player_info['foe'] = foes[0]


    def pump(self):
        # Physics are performed based on a fixed time step
        # or time scale from which all bodies on a scene
        # are ruled. This is done for consistent client-server
        # physics.
        self._ent_mgr.step(self._timescale)

        # Tell the EntityManager to deliver all
        # pending messages (if there are any)
        self._ent_mgr.dispatch_messages()

        # Pump network traffic
        super().pump()


    def on_data_received(self, data, host, port):
        """Pump network requests from clients

        Args:
            data(dict): incoming raw data
            host(str): client address
            port(int): client port
        """

        #
        # Get a nice Request from raw data
        #
        request = Request(data)

        #
        # By default, the server will not be OK with the incoming request
        #
        response = Response()
        response.status = Response.STATUS_UNAUTHORIZED
        response.reason = Response.REASON_CONN_REFUSED

        # TODO: Check for protocol version
        # if request.proto_version != Packet.PROTO_VERSION:
        #     # Send the packet to the client
        #     response.reason.REASON_VERSION_NOT_SUPPORTED
        #     self.send(response.data, host, port)
        #     return

        #######################################
        # The actual pump
        #######################################
        if request.command is not None:
            if request.player_id is None:
                #
                # Client is trying to establish a connection
                #
                if request.command == Request.CMD_CONNECT:
                    if len(self._players) < self.MAX_PLAYERS:
                        response.status = Response.STATUS_OK
                        response.reason = Response.REASON_CONN_GRANTED
                        response.player_id = self.create_player(host, port).uuid
                        self.update_players()

            elif request.player_id in self._players:
                #
                # Request is valid and going to be processed
                #

                # TODO: remove this when logger has been implemented
                #print("~> {}".format(request.data))

                # First of all, get the players' entities
                player_me = self._players[request.player_id]['entity']

                # FIXME: this will get better
                if self._players[request.player_id]['foe'] is not None:
                    foe_uuid = self._players[request.player_id]['foe']
                    player_foe = self._players[foe_uuid]['entity']


                # Get player's command
                command = request.command

                # +move command
                if command == Request.CMD_MV_UP:
                    player_me.apply_impulse((0 , self._paddle_impulse))

                # -move command
                elif command == Request.CMD_MV_DN:
                    player_me.apply_impulse((0, - self._paddle_impulse))

                # update command
                elif command == Request.CMD_UPDATE:
                    response.set_player_info(
                        name='you', score=0,
                        position=(int(player_me.position.x),
                                  int(player_me.position.y)),
                        velocity=(int(player_me.velocity.x),
                                  int(player_me.velocity.y))
                    )

                    # FIXME:
                    if self._players[request.player_id]['foe'] is not None:
                        response.set_player_info(
                            name='foe', score=0,
                            position=(int(player_foe.position.x),
                                      int(player_foe.position.y)),
                            velocity=(int(player_foe.velocity.x),
                                      int(player_foe.velocity.y))
                        )

                    response.set_ball_info(
                        position=(int(self._ball.position.x),
                                  int(self._ball.position.y)),
                        velocity=(int(self._ball.velocity.x),
                                  int(self._ball.velocity.y))
                    )

                # Set the answer as accepted
                response.status = Response.STATUS_OK
                response.reason = Response.REASON_ACCEPTED

                # TODO: remove this when logger has been implemented
                print("<~ {}".format(response.data))

        # Send the packet to the client
        self.send(response.data, host, port)
