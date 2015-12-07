# -*- coding: utf-8 -*-

"""
ming.ubjson
~~~~~~~~
Implementation of ming objects for BSON traffic

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import simpleubjson


class UbJsonCodec:
    def encode(self, data):
        return simpleubjson.encode(data)

    def decode(self, data):
        decoded_data = simpleubjson.decode(data)
        try:
            ddata = dict(decoded_data)
        except TypeError:
            ddata = list(decoded_data)

        return ddata
