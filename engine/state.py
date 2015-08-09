# -*- coding: utf-8 -*-

import pyglet

class State():
    """State implementation"""
    def __init__(self, *, machine):
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

class StateMachine(pyglet.event.EventDispatcher):
    """Finite state machine"""
    def __init__(self):
        super().__init__()

        #
        self.register_event_type('on_begin')
        self.register_event_type('on_run')
        self.register_event_type('on_exit')

        #
        self.stack = []
        self.states = {}

    def register_state(self, id, cls):
        self.states[id] = cls

    def get_current_state(self):
        if len(self.stack):
            return self.stack[0]
        return None

    def run_state(self):
        self.dispatch_event('on_run')

    def purge_stack(self):
        while len(self.stack):
            self.pop_state()

    def pop_state(self):
        self.dispatch_event('on_exit')
        self.stack.pop(0)
        self._attach_events(self.get_current_state())

    def _attach_events(self, state):
        if self._event_stack:
            self.pop_handlers()
        if state is not None:
            self.set_handler('on_begin', state.on_begin)
            self.set_handler('on_run', state.on_run)
            self.set_handler('on_exit', state.on_exit)

    def push_state(self, id):
        #
        state = self.get_current_state()
        if state is not None:
            self.dispatch_event('on_exit')

        #
        state = self.states[id](machine=self)

        #
        self.stack.insert(0, state)
        self._attach_events(state)

        #
        self.dispatch_event('on_begin')
