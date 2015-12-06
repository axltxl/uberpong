# -*- coding: utf-8 -*-

"""
game.entities.ball
~~~~~~~~
Ball as an entity

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

from uberpong.engine.spot import spot_get
from uberpong.engine.entity import Entity


class Ball(Entity):
    """Ball as an entity"""

    CTYPE = 40  # collision type

    def __init__(self, uuid, **kwargs):
        # call my parent
        super().__init__(uuid, mass=spot_get('sv_ball_mass'),
                         size=spot_get('ball_size'), **kwargs)

        # pymunk.Body elasticity for this paddle
        self.box.elasticity = 1.0

        # Ball top speed
        self.velocity_limit = spot_get('sv_ball_max_velocity')

        # Collision type for this body
        self.box.collision_type = self.CTYPE
