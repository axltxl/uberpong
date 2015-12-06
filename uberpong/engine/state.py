# -*- coding: utf-8 -*-

"""
engine.state
~~~~~~~~
A simple state system

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet


class State:
    """State implementation"""
    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): machine to manage this state
        """
        self._machine = machine

    @property
    def window(self):
        return self._machine.window

    #
    # Operations done on parent machine
    #
    def pop(self):
        self._machine.pop_state()

    def pop_until(self, class_id):
        self._machine.pop_until(class_id)

    def push(self, class_id):
        self._machine.push_state(class_id)

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

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
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

        # Set keyboard+mouse callbacks
        self._state_on_key_press = None
        self._state_on_key_release = None
        self._state_on_mouse_motion = None
        self._state_on_mouse_drag = None
        self._state_on_mouse_press = None
        self._state_on_mouse_release = None
        self._state_on_mouse_scroll = None

        # Attach pyglet.window input events to this state machine
        self._window.on_key_press = self._window_on_key_press
        self._window.on_key_release = self._window_on_key_release
        self._window.on_mouse_motion = self._window_on_mouse_motion
        self._window.on_mouse_drag = self._window_on_mouse_drag
        self._window.on_mouse_press = self._window_on_mouse_press
        self._window.on_mouse_release = self._window_on_mouse_release
        self._window.on_mouse_scroll = self._window_on_mouse_scroll

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

    def pop_until(self, class_id):
        """Pop states from the class until the first occurrence
        of an instance of class_id"""

        if class_id not in self._states:
            return

        while len(self._states) \
            and not isinstance(
                self.get_current_state(),
                self._states[class_id]
            ):
            self.pop_state()

    def pop_state(self):
        """Pop the state on top of the stack"""
        if len(self._stack):
            self.dispatch_event('on_exit')
            self._stack.pop(0)
            self._attach_events(self.get_current_state())

        # Trigger an on_begin event on new state
        self.dispatch_event('on_begin')

    def _attach_events(self, state):
        """Attach events (including window events) on state"""

        # Clean up window events attached to any current state
        self._state_on_key_press = None
        self._state_on_mouse_motion = None
        self._state_on_mouse_drag = None
        self._state_on_mouse_press = None
        self._state_on_mouse_release = None
        self._state_on_mouse_scroll = None

        if state is not None:
            # Assign this machine's events
            self.set_handler('on_begin', state.on_begin)
            self.set_handler('on_update', state.on_update)
            self.set_handler('on_exit', state.on_exit)

            # Assign state machine input events to the current state
            self._state_on_key_press = state.on_key_press
            self._state_on_key_release = state.on_key_release
            self._state_on_mouse_motion = state.on_mouse_motion
            self._state_on_mouse_drag = state.on_mouse_drag
            self._state_on_mouse_press = state.on_mouse_press
            self._state_on_mouse_release = state.on_mouse_release
            self._state_on_mouse_scroll = state.on_mouse_scroll

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

    #
    # Internal callbacks to be invoked by pyglet.window
    # input events
    #

    def _window_on_key_press(self, symbol, modifiers):
        self.on_key_press(symbol, modifiers)
        if self._state_on_key_press is not None:
            self._state_on_key_press(symbol, modifiers)

    def _window_on_key_release(self, symbol, modifiers):
        self.on_key_release(symbol, modifiers)
        if self._state_on_key_release is not None:
            self._state_on_key_release(symbol, modifiers)

    def _window_on_mouse_motion(self, x, y, dx, dy):
        self.on_mouse_motion(x, y, dx, dy)
        if self._state_on_mouse_motion is not None:
            self._state_on_mouse_motion(x, y, dx, dy)

    def _window_on_mouse_press(self, x, y, button, modifiers):
        self.on_mouse_press(x, y, button, modifiers)
        if self._state_on_mouse_press is not None:
            self._state_on_mouse_press(x, y, button, modifiers)

    def _window_on_mouse_release(self, x, y, button, modifiers):
        self.on_mouse_release(x, y, button, modifiers)
        if self._state_on_mouse_release is not None:
            self._state_on_mouse_release(x, y, button, modifiers)

    def _window_on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        if self._state_on_mouse_drag is not None:
            self._state_on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def _window_on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.on_mouse_scroll(x, y, scroll_x, scroll_y)
        if self._state_on_mouse_scroll:
            self._state_on_mouse_scroll(x, y, scroll_x, scroll_y)

    #
    # Input-related callbacks to be invoked by pyglet.window
    #

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
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
