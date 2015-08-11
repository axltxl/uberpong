# -*- coding: utf-8 -*-

"""
engine.spot
~~~~~~~~
Single Point Of Truth

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

_spot = {}

def spot_get(key):
    return _spot[key]

def spot_set(key, value):
    global _spot
    _spot[key] = value
    return value
