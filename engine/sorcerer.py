# -*- coding: utf-8 -*-

"""
engine.sorcerer
~~~~~~~~
Resource manager

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

class Sorcerer:
    def __init__(self):
        self._resources = {}
        self._root = 'assets/' # TODO: this has to change!
        self._root_fonts = '{}/fonts/'.format(self._root)

    def get_resource(self, key):
        if key in self._resources:
            return self._resources[key]
        return None


    def _push_resource(self, key, r):
        if key not in self._resources:
            self._resources[key] = r


    def create_font(self, key, *, file_name):
        pyglet.font.add_file('{}/{}'.format(self._root_fonts, file_name))
        self._push_resource(key, pyglet.font.load(key))
