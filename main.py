#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from game.game import Game

if __name__=='__main__':
    sys.exit(Game(sys.argv[1:]).go())
