# -*- coding: utf-8 -*-

from engine.entity import Entity

class PlayerEntity(Entity):
    def __init__(self, uuid, **kwargs):
        super().__init__(uuid, size=(32, 64), **kwargs)
