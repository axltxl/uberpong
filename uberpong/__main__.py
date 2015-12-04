# -*- coding: utf-8 -*-

"""
uberpong.__main__
~~~~~~~~
Game main entry point

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""

import sys
from uberpong.game.game import Game

if __name__=='__main__':
    sys.exit(Game(sys.argv[1:]).go())
