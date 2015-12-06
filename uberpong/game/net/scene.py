# -*- coding: utf-8 -*-

"""
game.net.scene
~~~~~~~~
Client implementation for a player

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import pyglet

import uberpong.ming as ming
from uberpong.engine.spot import spot_get
from uberpong.engine.entity import EntityManager

from . import (
    Request,
    Response
)

from ..entities import (
    PlayerPaddle,
    Board,
    Ball
)


class Scene(ming.Server):
    """
    Scene server implementation

    This bad boy handles the game per se, by keeping and
    controlling entities and pumping responses to clients so
    they can do their rendering.
    """

    # Maximum number of players (clients) allowed to join the game
    MAX_PLAYERS = 2

    # States
    ST_WAITING_FOR_PLAYER = 100
    ST_BEGIN = 101
    ST_PLAYING = 102
    ST_SCORE = 103
    ST_GAME_SET = 104

    def __init__(self, *, width, height, **kwargs):
        """Constructor

        Kwargs:
            width(int): width of the scene in pixels
            height(int): height of the scene in pixels
            kwargs(dict, optional): Arbitrary keyword arguments
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

        # Paddle impulse, top speed and artificial friction
        self._paddle_impulse = spot_get('sv_paddle_impulse')
        self._paddle_max_velocity = spot_get('sv_paddle_max_velocity')
        self._paddle_friction = spot_get('sv_paddle_friction')

        # Create the actual ball
        self.create_ball()

        # Current state
        self._state = self.ST_WAITING_FOR_PLAYER

        # Set up tick interval on server
        self._tickrate = 1.0 / spot_get('tickrate')
        pyglet.clock.schedule_interval(self.tick, self._tickrate)

        # this method wis called each time the ball
        # collides with either the left or the right boundary
        # on the board
        self._ent_mgr.add_collision_handler(
            Ball.CTYPE, Board.BOUNDARY_CTYPE_LEFT,
            begin=self._scored_left
        )
        self._ent_mgr.add_collision_handler(
            Ball.CTYPE, Board.BOUNDARY_CTYPE_RIGHT,
            begin=self._scored_right
        )

    def _scored_left(self, space, arbiter, *args, **kwargs):
        """ the ball has collided with the left boundary """
        player = [p for p in self._players.values() if p.number == 2][0]
        player.score += 1  # bump the score
        self._scored()
        return False  # tell pymunk to ignore the collision

    def _scored_right(self, space, arbiter, *args, **kwargs):
        """ the ball has collided with the right boundary """
        player = [p for p in self._players.values() if p.number == 1][0]
        player.score += 1  # bump the score
        self._scored()
        return False  # tell pymunk to ignore the collision

    def _scored(self):
        """
        At this point , the ball has collided with
        either the right or left wall
        """
        # Set state to 'score' state
        self._state = self.ST_SCORE

        # Wait for 3 seconds before unfreezing the board
        # If one of the players has reached max score, then switch
        # to set state, otherwise, go back to round state
        pyglet.clock.schedule_once(self._round_goback, 3)

    def _round_goback(self, dt):
        if any([player.score == spot_get('sv_score_max')
               for player in self._players.values()]):
            self._state = self.ST_GAME_SET
        else:
            self._state = self.ST_PLAYING

    @property
    def state(self):
        """Get current state in server"""
        return self._state

    def broadcast_update(self):
        """Send an update to all clients"""

        if len(self._players):
            # The actual response
            response = Response()

            # Set the answer as accepted
            response.status = Response.STATUS_OK
            response.reason = Response.REASON_UPDATE

            # Set state
            response.state = self._state

            for player in self._players.values():
                # Current player
                player_me = player

                # Get host and port from him
                host = player.host
                port = player.port

                if self._state == self.ST_PLAYING \
                or self.state == self.ST_SCORE \
                or self.state == self.ST_BEGIN:
                    # Set player information
                    response.set_player_info(
                        name='you',
                        score=player_me.score,
                        number=player_me.number,
                        position=(int(player_me.position.x),
                                  int(player_me.position.y)),
                        velocity=(int(player_me.velocity.x),
                                  int(player_me.velocity.y))
                    )

                    # Set opponent (foe) information
                    if player.foe is not None:

                        player_foe = self._players[player.foe]

                        response.set_player_info(
                            name='foe',
                            score=player_foe.score,
                            number=player_foe.number,
                            position=(int(player_foe.position.x),
                                      int(player_foe.position.y)),
                            velocity=(int(player_foe.velocity.x),
                                      int(player_foe.velocity.y))
                        )

                    # Set ball information
                    response.set_ball_info(
                        position=(int(self._ball.position.x),
                                  int(self._ball.position.y)),
                        velocity=(int(self._ball.velocity.x),
                                  int(self._ball.velocity.y))
                    )

                # Send the packet to the client
                self.send(response.data, host, port)

    def _reset_player(self, player):
        """Reset values on a player"""

        # Calculate initial position
        player_position_x, player_position_y = spot_get('paddle_position_start')

        # player 2's position on the other side of the screen
        if player.number == 2:
            player_position_x = self._window_width - player_position_x

        # Set initial position for this player
        player.position = player_position_x, player_position_y

        # Reset physics on this player
        # player.reset_forces()
        player.velocity = (0, 0)

        if self._state == self.ST_BEGIN:
            # Reset score
            player.score = 0

            # Ready state for this player
            player.ready = False

    def reset_players(self):
        """Reset values on players"""

        for player in self._players.values():
            self._reset_player(player)

    def reset_ball(self):
        """Reset ball position"""

        # Set initial position for this ball
        # self._ball.reset_forces()
        self._ball.velocity = (0, 0)
        self._ball.position = spot_get('ball_position_start')

        # FIXME: do something better
        # Set initial impulse on the ball
        self._ball.apply_impulse((-1500, 0))

    def create_ball(self):
        """Create a ball to play"""
        # New PlayerPaddle for a client
        self._ball = self._ent_mgr.create_entity('ent_ball')

        # Reset values on ball
        self.reset_ball()

        # Increase/maintain ball velocity each second
        # TODO: move this to tick()
        pyglet.clock.schedule_interval(self.increase_ball_velocity, 1.0)

    def create_player(self, host, port):
        """Create a PlayerPaddle for a client

        Args:
            host(str): client address
            port(int): client port
        """

        # New PlayerPaddle for a client
        player = self._ent_mgr.create_entity(
            'ent_player',
            host=host,
            port=port,
            number=len(self._players) + 1,
        )

        # Add this player to the server
        self._players[player.uuid] = player

        # Reset its values
        self._reset_player(self._players[player.uuid])

        # Return the entity
        return player

    def destroy_player(self, player_id):
        """Get rid of a player"""
        del self._players[player_id]

    def update_players(self):
        """Update information on players"""

        # Change state depending on the number of players present
        if len(self._players) < self.MAX_PLAYERS:
            self._state = self.ST_WAITING_FOR_PLAYER
        else:
            self._state = self.ST_BEGIN

        # Update each player's foes
        for uuid, player in self._players.items():
            foes = [p.uuid for p in self._players.values() if p.uuid != uuid]
            if len(foes):
                player.foe = foes[0]
            else:
                player.foe = None

    def increase_ball_velocity(self, dt):
        """Increase/maintain a constant velocity for the ball"""

        if self._state == self.ST_PLAYING:
            # In order to have a decent/pleasurable gameplay
            # the ball needs to maintain a certain pace, so it
            # becomes "pushed" constantly until it reaches its
            # top speed
            self._ball.velocity = (1.02 * self._ball.velocity.x,
                                   1.02 * self._ball.velocity.y)

            # Very much like table hockey games the ball gets
            # pushed until it gains its minimun speed of 200.0
            if abs(self._ball.velocity.x) < 200.0:
                if self._ball.velocity.x > 0:
                    self._ball.apply_impulse((200, self._ball.velocity.y))
                elif self._ball.velocity.x < 0:
                    self._ball.apply_impulse((-200, self._ball.velocity.y))

    def tick(self, dt):
        """Run simulation on server and broadcast an update to all clients

        During each tick, the server processes incoming user commands,
        runs a physical simulation step, checks the game rules,
        and updates all object states.
        """

        # Process incoming user commands
        self.pump()

        #################################
        # Run a physical simulation step:
        #################################

        if self._state == self.ST_PLAYING:
            # FIXME: This is working, it caps the velocity to 0 in x
            # so it won't move sideways no matter what
            for player in self._players.values():

                # cancel horizontal velocity
                player.velocity = 0, player.velocity.y

                # artificial friction maybe?
                player.apply_impulse(
                    (0, - self._paddle_friction * player.velocity.y)
                )

            # Physics are performed based on a fixed time step
            # or time scale from which all bodies on a scene
            # are ruled. This is done for consistent client-server
            # physics.
            self._ent_mgr.step(self._tickrate)

            # Tell the EntityManager to deliver all
            # pending messages (if there are any)
            self._ent_mgr.dispatch_messages()

        elif self._state == self.ST_BEGIN:
            # If all players are ready, then move on
            if all([p.ready for p in self._players.values()]):
                self._state = self.ST_PLAYING

        # Broadcast latest snapshot to all clients
        self.broadcast_update()

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
        request = Request(data=data)

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

                        # Send the packet to the client
                        self.send(response.data, host, port)

            elif request.player_id in self._players:
                #
                # Request is valid and going to be processed
                #

                # First of all, get the players' entities
                player_me = self._players[request.player_id]

                # FIXME: this will get better
                if self._players[request.player_id].foe is not None:
                    foe_uuid = self._players[request.player_id].foe
                    player_foe = self._players[foe_uuid]

                # Get player's command
                command = request.command

                # TODO: document this
                if self._state == self.ST_PLAYING:

                    # +move command
                    if command == Request.CMD_MV_UP:
                        player_me.apply_impulse((0, self._paddle_impulse))

                    # -move command
                    elif command == Request.CMD_MV_DN:
                        player_me.apply_impulse((0, - self._paddle_impulse))

                # TODO: document this
                if self._state == self.ST_BEGIN:

                    # +ready command
                    if command == Request.CMD_READY:
                        player_me.ready = True

                # disconnect command
                if command == Request.CMD_DISCONNECT:
                    self.destroy_player(request.player_id)
                    self.update_players()
