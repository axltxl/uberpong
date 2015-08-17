# -*- coding: utf-8 -*-

"""
game.entities.ball
~~~~~~~~
Ball as an entity

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

from engine.spot import spot_get
from engine.entity import Entity

class Ball(Entity):
    """Ball as an entity"""

    def __init__(self, uuid, **kwargs):
        # call my parent
        super().__init__(uuid, size=spot_get('ball_size'), **kwargs)

        # pymunk.Body elasticity for this paddle
        self.box.elasticity = 1.0
