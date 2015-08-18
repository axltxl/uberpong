# -*- coding: utf-8 -*-

"""
game.entities.player
~~~~~~~~

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

from engine.spot import spot_get
from engine.entity import Entity

from game.entities.ball import Ball

class PlayerPaddle(Entity):
    """Paddle as an entity"""

    CTYPE = 50  # collision type

    def __init__(self, uuid, **kwargs):
        """Constructor"""

        # call my parent
        super().__init__(uuid, mass=spot_get('sv_paddle_mass'),
                         size=spot_get('paddle_size'), **kwargs)

        # pymunk.Body elasticity for this paddle
        self.box.elasticity = 1.0

        # collision type for this body
        self.box.collision_type = self.CTYPE

        # paddle top speed
        self.velocity_limit = spot_get('sv_paddle_max_velocity')

        # TODO: to be used later
    #     self.manager.add_collision_handler(self.CTYPE,
    #         Ball.CTYPE, separate=self._volley)
    #
    # def _volley(self, space, arbiter, *args, **kwargs):
    #     ball = [b for b in arbiter.shapes if b.collision_type == Ball.CTYPE][0].body
        #import ipdb; ipdb.set_trace()
        #arbiter.elasticity = 4.0
        #ball.apply_impulse((50000000000 * ball.velocity.x, 50000000000 * ball.velocity.y))
        #return True
