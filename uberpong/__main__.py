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

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    return Game(sys.argv[1:]).go()

if __name__=='__main__':
    sys.exit(main())
