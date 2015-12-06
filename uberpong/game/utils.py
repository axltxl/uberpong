# -*- coding: utf-8 -*-

"""
game.utils
~~~~~~~~
Utilities used throughout the entire game

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import pyglet
from . import colors

FONT_PRIMARY = '8-bit Operator+'
FONT_SECONDARY = '8-bit Operator+ 8'


def create_label(text='', *,
                 window,
                 font_size=15,
                 x=None, y=None,
                 bold=False,
                 font_name=FONT_PRIMARY,
                 anchor_x='center',
                 anchor_y='center'):
    """ Create a pyglet label easily

    Args:
        text(str): Initial text for this resource

    Kwargs:
        font_size(int, optional): font size
        x(int, optional): horizontal position
        y(int, optional): vertical position
        bold(bool, optional): whether or not this label is going to be rendered as bold text
        anchor_x(int, optional): horizontal anchor for this label
        anchor_y(int), optional: vertical anchor for this label
    """

    # by default, a label created under this method
    # is going to be centered if no position has been specified
    if x is None:
        pos_x = window.width // 2
    else:
        pos_x = x

    if y is None:
        pos_y = window.height // 2
    else:
        pos_y = y

    # create the actual thing
    label = pyglet.text.Label(
        text, font_name=font_name, font_size=font_size,
        x=pos_x, y=pos_y, bold=bold,
        anchor_x=anchor_x, anchor_y=anchor_y
    )
    label.set_style('color', colors.GRAY0 + (255,))

    # give the label
    return label
