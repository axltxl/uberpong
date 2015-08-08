# -*- coding: utf-8 -*-

from .state import StateMachine

class EntityManager():
    def __init__(self):
        self.entities = []

class Entity(StateMachine):
    """docstring for Entity(arg)"""
    def __init__(self):
        super.__init__(self)
