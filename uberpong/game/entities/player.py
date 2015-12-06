# -*- coding: utf-8 -*-

"""
game.entities.player
~~~~~~~~

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

from uberpong.engine.spot import spot_get
from uberpong.engine.entity import Entity


class PlayerPaddle(Entity):
    """Paddle as an entity"""

    CTYPE = 50  # collision type

    def __init__(self,
                 uuid,
                 host=None,
                 port=None,
                 number=None,
                 foe=None,
                 **kwargs):
        """Constructor

        Kwargs:
            host(str): Client address associated with this player
            port(str): Source port of client address
            number(int): Player number
            foe(str): Opponent UUID
        """

        # call my parent
        super().__init__(uuid, mass=spot_get('sv_paddle_mass'),
                         size=spot_get('paddle_size'), **kwargs)

        # pymunk.Body elasticity for this paddle
        self.box.elasticity = 1.0

        # collision type for this body
        self.box.collision_type = self.CTYPE

        # paddle top speed
        self.velocity_limit = spot_get('sv_paddle_max_velocity')

        # Networking information for this player
        self.host = host
        self.port = port

        # Player number
        self.number = number

        # This player's opponent
        self.foe = foe

        # Initial flags for this player
        self.ready = False
        self.score = 0
