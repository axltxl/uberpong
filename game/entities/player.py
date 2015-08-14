# -*- coding: utf-8 -*-

"""
game.entities.player
~~~~~~~~

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


from engine.entity import Entity


class PlayerEntity(Entity):
    """Player as an entity"""

    def __init__(self, uuid, **kwargs):
        """Constructor"""
        super().__init__(uuid, size=(32, 64), **kwargs)
        self.friction = 2.0
