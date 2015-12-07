# -*- coding: utf-8 -*-

"""
game.entities.board
~~~~~~~~
Board as an entity

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import pymunk


class Board:
    """The game board itself"""

    BOUNDARY_CTYPE_LEFT = 80  # collision type for left wall
    BOUNDARY_CTYPE_RIGHT = 81  # collision type for right wall

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
        self._body = pymunk.Body()  # static body
        self._body.position = 0, 0

        # Coordinates used to create segments
        left = 0
        top = height - 1
        right = width - 1
        bottom = 0
        thick = 200  # thickness of walls

        # Create the actual static boundaries
        # everything inside these boundaries will collide with them
        #
        #
        #           (left,top)             (right,top)
        #                  *--------------*
        #                  |              |
        #                  |              |
        #                  |              |
        #                  |              |
        #                  |              |
        #                  *--------------*
        #           (left,bottom)          (right,bottom)
        #
        boundaries = {
            'up': pymunk.Poly(self._body, [
                (left - thick, top),
                (right + thick, top),
                (right + thick, top + thick),
                (left - thick, top + thick),
            ]),

            'down': pymunk.Poly(self._body, [
                (left - thick, bottom - thick),
                (right + thick, bottom - thick),
                (right + thick, bottom),
                (left - thick, bottom),
            ]),

            'left': pymunk.Poly(self._body, [
                (left - thick, bottom),
                (left, bottom),
                (left, top),
                (left - thick, top),
            ]),

            'right': pymunk.Poly(self._body, [
                (right, bottom),
                (right + thick, bottom),
                (right + thick, top),
                (right, top),
            ])
        }

        # left and right boundaries need to have their
        # collision type specified, these walls are the
        # to know whether has scored
        boundaries['left'].collision_type = self.BOUNDARY_CTYPE_LEFT
        boundaries['right'].collision_type = self.BOUNDARY_CTYPE_RIGHT

        for boundary in boundaries.values():
            # elasticity for each boundary
            boundary.elasticity = 1.0

            # Put them in the space
            self._space.add(boundary)
