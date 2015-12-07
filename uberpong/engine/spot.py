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
    """Get value under key

    Args:
        key(str): name of value
    Returns:
        Value stored under 'key', otherwise None
    """
    if key in _spot:
        return _spot[key]
    return None


def spot_set(key, value):
    """Set value under key

    Args:
        key(str): Name of new or existing key
        value(str): New value for key
    Returns:
        Value set
    """
    global _spot
    _spot[key] = value
    return value
