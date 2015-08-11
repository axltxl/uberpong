# -*- coding: utf-8 -*-

"""
engine.system
~~~~~~~~
A simple state system

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet

class State():
    """State implementation"""
    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): machine to manage this state
        """
        self._machine = machine

    #
    # Operations done on parent machine
    #
    def pop(self):
        self._machine.pop()

    def push(self, id):
        self._machine.push(id)

    #
    # Callbacks to be invoked by events in the parent machine
    #
    def on_begin(self):
        """
        This is going to be called after this state has been created
        and pushed onto its parent machine's stack
        """
        pass

    def on_update(self):
        """Triggered on every iteration in the main event loop"""
        pass

    def on_exit(self):
        """
        Triggered before this state is popped out its parent machine's stack
        or just before a new state is pushed onto it
        """
        pass

    #
    # Input-related callbacks to be invoked by pyglet.window
    #

    def on_key_press(self, sym, mod):
        pass

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
        """Constructor

        Kwargs:
            window(pyglet.window): a pyglet.window instance to attach events
        """
        super().__init__()

        # Register basic event types
        self.register_event_type('on_begin')
        self.register_event_type('on_update')
        self.register_event_type('on_exit')

        # State stack
        self._stack = []

        # Registered state classes
        self._states = {}

        # window
        self._window = window

    @property
    def window(self):
        return self._window

    def register_state(self, class_id, cls):
        """Register State class

        Args:
            class_id(str): key name for this State class
            cls(class): The actual State class
        """
        self._states[class_id] = cls

    def get_current_state(self):
        """Return current state on top of stack

        Returns:
            A State, if the stack is empty it will return None
        """
        if len(self._stack):
            return self._stack[0]
        return None

    def update_state(self):
        """Raise on_update event on the state currently active"""
        self.dispatch_event('on_update')

    def purge_stack(self):
        """Pop all states from the stack"""
        while len(self._stack):
            self.pop_state()

    def pop_state(self):
        """Pop the state on top of the stack"""
        self.dispatch_event('on_exit')
        self._stack.pop(0)
        self._attach_events(self.get_current_state())

    def _attach_events(self, state):
        """Attach events (including window events) on state"""

        # Workaround to know whether events should be disposed first
        if self._event_stack:
            self.pop_handlers()

        # Clean up window events attached to any current state
        self._window.on_key_press = None
        self._window.on_mouse_motion = None
        self._window.on_mouse_drag = None
        self._window.on_mouse_press = None
        self._window.on_mouse_release = None
        self._window.on_mouse_scroll = None

        if state is not None:
            # Assign this machine's events
            self.set_handler('on_begin', state.on_begin)
            self.set_handler('on_update', state.on_update)
            self.set_handler('on_exit', state.on_exit)

            # Assign window events
            self._window.on_key_press = state.on_key_press
            self._window.on_mouse_motion = state.on_mouse_motion
            self._window.on_mouse_drag = state.on_mouse_drag
            self._window.on_mouse_press = state.on_mouse_press
            self._window.on_mouse_release = state.on_mouse_release
            self._window.on_mouse_scroll = state.on_mouse_scroll

    def push_state(self, class_id):
        """Push a new state onto the stack

        Args:
            class_id(str): registered class id
        """
        # Get state at the top of the stack and raise an on_exit event
        state = self.get_current_state()
        if state is not None:
            self.dispatch_event('on_exit')

        # Create a new state
        state = self._states[class_id](machine=self)

        # Push this new state onto the stack and attach
        # events onto it
        self._stack.insert(0, state)
        self._attach_events(state)

        # Trigger an on_begin event on new state
        self.dispatch_event('on_begin')
