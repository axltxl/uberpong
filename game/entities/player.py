# -*- coding: utf-8 -*-

"""
game.entities.player
~~~~~~~~

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

from engine.spot import spot_get
from engine.entity import Entity

class PlayerPaddle(Entity):
    """Paddle as an entity"""

    def __init__(self, uuid, **kwargs):
        """Constructor"""

        # call my parent
        super().__init__(uuid, mass=spot_get('sv_paddle_mass'),
                         size=spot_get('paddle_size'), **kwargs)

        # pymunk.Body elasticity for this paddle
        self.box.elasticity = 1.0
