# -*- coding: utf-8 -*-

"""
ming.json
~~~~~~~~
Implementation of ming objects for JSON traffic

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import json

class JsonCodec:
    def encode(self, data):
        return bytes(json.dumps(data, separators=(',', ':')), 'utf-8')

    def decode(self, data):
        return json.loads(data.decode('utf-8'))
