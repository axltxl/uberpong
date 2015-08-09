# -*- coding: utf-8 -*-

import pyglet

class State():
    """State implementation"""
    def __init__(self, *, machine):
        self.machine = machine

    #
    #
    #
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

    #
    #
    #
    def on_key_press(self, sym, mod):
        pass

    #
    #
    #
    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass


class StateMachine(pyglet.event.EventDispatcher):
    """Finite state machine"""
    def __init__(self, *, window):
        super().__init__()

        #
        self.register_event_type('on_begin')
        self.register_event_type('on_run')
        self.register_event_type('on_exit')

        #
        self.stack = []
        self.states = {}

        # window
        self.window = window

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
        #
        if self._event_stack:
            self.pop_handlers()

        # cleanup window events attached to any current state
        self.window.on_key_press = None

        self.window.on_mouse_motion = None
        self.window.on_mouse_drag = None
        self.window.on_mouse_press = None
        self.window.on_mouse_release = None
        self.window.on_mouse_scroll = None


        if state is not None:
            #
            self.set_handler('on_begin', state.on_begin)
            self.set_handler('on_run', state.on_run)
            self.set_handler('on_exit', state.on_exit)

            #
            # window events
            #
            self.window.on_key_press = state.on_key_press

            self.window.on_mouse_motion = state.on_mouse_motion
            self.window.on_mouse_drag = state.on_mouse_drag
            self.window.on_mouse_press = state.on_mouse_press
            self.window.on_mouse_release = state.on_mouse_release
            self.window.on_mouse_scroll = state.on_mouse_scroll

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
