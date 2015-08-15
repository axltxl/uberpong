# -*- coding: utf-8 -*-

"""
game.entities.board
~~~~~~~~
Board as an entity

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


#from engine.entity import Entity
import pymunk

class Board:
    """Board as an entity"""
    def __init__(self, width, height, space):

        # TODO: document this!
        self._space = space

        # TODO: document this!
        self._body = pymunk.Body() # static body
        self._body.position = 0, 0

        # TODO: document this!
        left = 0
        top = height + 1
        right = width
        bottom = 0
        thick = 0.0  # thickness of segments

        # TODO: document this!
        boundaries = [
            pymunk.Segment(self._body, (left,top), (right,top), thick),  # up
            pymunk.Segment(self._body, (left,bottom), (right,bottom), thick),  # down
            pymunk.Segment(self._body, (left,top), (left,bottom), thick),  # left
            pymunk.Segment(self._body, (right,top), (right,bottom), thick)  # right
        ]

        # TODO: document this!
        # elasticity
        for b in boundaries:
            b.elasticity = 0.0

        # TODO: document this!
        self._space.add(boundaries)
