# -*- coding: utf-8 -*-

class State:
    """State implementation"""
    def __init__(self, id, *, machine):
        self.id = id
        self.machine = machine

    def pop(self):
        self.machine.pop()

    def push(self, id):
        self.machine.push(id)

    def on_begin(self):
        pass

    def on_run(self):
        pass

    def on_exit(self):
        pass

class StateMachine:
    """Finite state machine"""
    def __init__(self):
        self.stack = []
        self.states = {}

    def register(self, state):
        self.states[state.id] = state

    def _get_current_state(self):
        return self.stack[0]

    def pop(self):
        self._get_current_state().on_exit()
        self.stack.pop(0)

    def push(self, id):
        self._get_current_state().on_exit()
        self.stack.insert(0, self.states[id])
