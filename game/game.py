# -*- coding: utf-8 -*-

import pyglet
import sys, traceback, os
from engine.state import State, StateMachine
from engine.entity import EntityManager

GAME_NAME = "PONG!"
GAME_VER = "0.1a"


class GameSplash(State):
    """Game start state"""

    def __init__(self, *, machine):
        """Constructor

        Kwargs:
            machine(StateMachine): parent state machine
        """

        # Call my parent
        super().__init__(machine=machine)

        # Toggle flags
        self._show_press_start = True # This is used for _comp_label animation
        self._key_pressed = False # has been a key pressed?

        # This should be moved to another level
        pyglet.font.add_file('assets/fonts/8bitOperatorPlus-Regular.ttf')
        font_8bit_operator = pyglet.font.load('8-bit Operator+')

        # and this as well
        self.snd_begin = pyglet.media.load('assets/sounds/begin.wav', streaming=False)

        # Title label
        self._title_label = pyglet.text.Label(
            GAME_NAME, font_name='8-bit Operator+', font_size=72,
            x=machine.window.width//2, y=machine.window.height//2 + 16,
            anchor_x='center', anchor_y='center'
        )

        # Companion label
        self._comp_label = pyglet.text.Label(
            "Press ANY KEY to play!", font_name='8-bit Operator+', font_size=24,
            x=machine.window.width//2, y=machine.window.height//2 - 64,
            anchor_x='center', anchor_y='center'
        )


    def _toggle_press_start(self, dt):
        """Toggle _show_press_start flag"""
        self._show_press_start ^= True

    #
    # pyglet event callbacks
    #

    def on_begin(self):
        pyglet.clock.schedule_interval(self._toggle_press_start, 0.5)


    def on_update(self):
        # Draw labels
        self._title_label.draw()
        if self._show_press_start:
            self._comp_label.draw()


    def on_key_press(self, sym, mod):
        pyglet.clock.unschedule(self._toggle_press_start)
        self._key_pressed = True
        self._show_press_start = False

        #
        self.snd_begin.play()


class Game(StateMachine):
    """Game class"""

    def __init__(self, argv):
        #
        # Set up window
        #
        self._window = pyglet.window.Window(
            640, 480,
            style=pyglet.window.Window.WINDOW_STYLE_DIALOG,
            caption="{name} - {version}".format(name=GAME_NAME, version=GAME_VER)
        )
        self._window.on_draw = self.on_draw
        self._window.on_close = self.on_window_close

        #
        super().__init__(window=self._window)

        #
        self.register_state('game_splash', GameSplash)

        #
        self._shutdown = False

        #
        self._ent_mgr = EntityManager()


    def on_window_close(self):
        self._shutdown = True

    def on_draw(self):
        self._window.clear()
        self.update_state()

    def _handle_except(self, e):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Unhandled {e} at {file}:{line}: '{msg}'"
              .format(e=exc_type.__name__, file=fname,
              line=exc_tb.tb_lineno,  msg=e))
        print(traceback.format_exc())

    def go(self):
        """Main entry point"""
        try:
            # Push first State
            self.push_state('game_splash')

            # Run the thing!
            while not self._shutdown:
                #
                pyglet.clock.tick()

                #
                self._ent_mgr.dispatch_messages()

                #
                #self.run_state()

                #
                for window in pyglet.app.windows:
                    window.switch_to()
                    window.dispatch_events()
                    window.dispatch_event('on_draw')
                    window.flip()


        except Exception as e:
            self._handle_except(e)

        finally:
            self._cleanup()

        return 0

    def _cleanup(self):
        """House keeping after all's been done"""
        self.purge_stack()
