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
    """The game board itself"""

    def __init__(self, width, height, space):
        """Constructor

        A board consist of four boundary lines created from
        a static pymunk.Body using viewport (window) width and height,
        this environment will be used to make the game happen.

        Args:
            width(int): board width in pixels
            height(int): board height in pixels
            space(pymunk.Space): pymunk Space in which all physics are applied
        """

        # set the physics world
        self._space = space

        # Create a static body from which static segments (lines)
        # will be made and put onto the space
        self._body = pymunk.Body() # static body
        self._body.position = 0, 0

        # Coordinates used to create segments
        left = 0
        top = height + 1
        right = width
        bottom = 0
        thick = 0.0  # thickness of segments

        # Create the actual static segments
        # everything inside these boundary segments will collide with them
        #
        #
        #           (left,top)             (right,top)
        #                  *--------------*
        #                  |              |
        #                  |              |
        #                  |              |
        #                  *--------------*
        #           (left,bottom)          (right,bottom)
        #
        boundaries = [
            pymunk.Segment(self._body, (left,top), (right,top), thick),  # up
            pymunk.Segment(self._body, (left,bottom), (right,bottom), thick),  # down
            pymunk.Segment(self._body, (left,top), (left,bottom), thick),  # left
            pymunk.Segment(self._body, (right,top), (right,bottom), thick)  # right
        ]

        # elasticity for each boundary
        for b in boundaries:
            b.elasticity = 1.0

        # Put them in the space
        self._space.add(boundaries)
