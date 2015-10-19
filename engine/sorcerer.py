# -*- coding: utf-8 -*-

"""
engine.sorcerer
~~~~~~~~
Resource manager

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet
from os import path

class Sorcerer:
    """ A slightly useful resource manager """

    def __init__(self, *, root_dir):
        """Constructor

        Kwargs:
            root_dir(str): root directory for assets
        """
        # resources themselves
        self._resources = {}

        # root directory for assets
        self._root = path.abspath(root_dir)

        # fonts root directory
        self._root_fonts = path.join(self._root, 'fonts')


    def get_resource(self, key):
        """Get a resource

        Args:
            key(str): logical name for this resource
        """
        if key in self._resources:
            return self._resources[key]
        return None


    def _push_resource(self, key, r):
        if key not in self._resources:
            self._resources[key] = r


    def create_font(self, key, *, file_name):
        """Create a pyglet font

        Kwargs:
            file_name(str): font file to use
        """
        pyglet.font.add_file('{}/{}'.format(self._root_fonts, file_name))
        self._push_resource(key, pyglet.font.load(key))
