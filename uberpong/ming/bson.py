# -*- coding: utf-8 -*-

"""
ming.bson
~~~~~~~~
Implementation of ming objects for BSON traffic

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import bson

class BsonCodec:
    def encode(self, data):
        return bson.dumps(data)

    def decode(self, data):
        return bson.loads(data)
