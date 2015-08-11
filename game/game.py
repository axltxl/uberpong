# -*- coding: utf-8 -*-

"""
game.game
~~~~~~~~
Game main entry point

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import pyglet
import sys
import traceback
import os
from engine.state import State, StateMachine
from engine.entity import EntityManager
from engine.spot import spot_set, spot_get
from .states import splash

# Set initial SPOT values
spot_set('game_name', "PONG!")
spot_set('game_version', "0.1a")


class Game(StateMachine):
    """Game class"""

    def __init__(self, argv):
        #
        # Set up window
        #
        self._window = pyglet.window.Window(
            640, 480,
            style=pyglet.window.Window.WINDOW_STYLE_DIALOG,
            caption="{name} - {version}"
            .format(name=spot_get('game_name'),
                    version=spot_get('game_version'))
            )
        self._window.on_draw = self.on_draw
        self._window.on_close = self.on_window_close

        # Call the parent
        super().__init__(window=self._window)

        # Register states
        self.register_state('state_splash', splash.GameSplash)

        # Shutdown flag
        self._shutdown = False

        # Set up the actual EntityManager
        self._ent_mgr = EntityManager()

        # Register this object onto the SPOT
        spot_set('game_object', self)

    #
    # pyglet.window event methods
    #
    def on_window_close(self):
        self.exit()

    def on_draw(self):
        self._window.clear()
        self.update_state()

    def on_key_press(self, sym, mod):
        """Exit the game if F12 has been pressed"""
        if sym == pyglet.window.key.F12:
            self.exit()

    def _handle_except(self, e):
        """Exception handler"""
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Unhandled {e} at {file}:{line}: '{msg}'"
              .format(e=exc_type.__name__, file=fname,
              line=exc_tb.tb_lineno,  msg=e))
        print(traceback.format_exc())

    def exit(self):
        """Exit the game"""
        self._shutdown = True

    def go(self):
        """Main entry point"""
        try:
            # Push first State
            self.push_state('state_splash')

            # Run the thing!
            while not self._shutdown:
                #
                pyglet.clock.tick()

                # Tell the EntityManager to deliver all
                # pending messages (if there are any)
                self._ent_mgr.dispatch_messages()

                # pyglet.window bit
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
