# -*- coding: utf-8 -*-

"""
engine.sorcerer
~~~~~~~~
Resource manager

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


from os import path
import pyglet


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

        # sounds root directory
        self._root_sounds = path.join(self._root, 'sounds')

        # images root directory
        self._root_images = path.join(self._root, 'images')

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
        return r

    def create_font(self, key, *, file_name):
        """Create a pyglet font

        Kwargs:
            key(str): resource key name
            file_name(str): font file to use

        Returns:
            A new (if not existent) pyglet Font
        """
        # don't even bother to load if it's
        # already present on this sorcerer
        if key not in self._resources:
            pyglet.font.add_file('{}/{}'.format(self._root_fonts, file_name))
            self._push_resource(key, pyglet.font.load(key))

    def create_image(self, key, *, file_name):
        """Create a pyglet font

        Kwargs:
            key(str): resource key name
            file_name(str): font file to use

        Returns:
            A new (if not existent) pyglet Image
        """

        return self._push_resource(
            key,
            pyglet.image.load(
                '{}/{}'.format(
                    self._root_images, file_name
                )
            )
        )

    def create_sound(self, key, *, file_name):
        """Create a pyglet sound

        Kwargs:
            key(str): resource key name
            file_name(str): sound file to use

        Returns:
            A new (if not existent) pyglet Sound
        """

        return self._push_resource(
            key,
            pyglet.media.load(
                '{}/{}'.format(
                    self._root_sounds,
                    file_name
                )
            )
        )
