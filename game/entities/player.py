# -*- coding: utf-8 -*-

"""
game.entities.player
~~~~~~~~

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


from engine.entity import Entity

# FIXME: Rename as PlayerPaddle
class PlayerEntity(Entity):
    """Player as an entity"""

    def __init__(self, uuid, **kwargs):
        """Constructor"""

        # FIXME: Paddle size should be set on SPOT tuple 'paddle_size' ?
        super().__init__(uuid, size=(32, 64), **kwargs)

        # TODO: document this!
        self.rect.elasticity = 0.0
