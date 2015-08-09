# -*- coding: utf-8 -*-

import pyglet
import sys, traceback
from engine.state import State, StateMachine

class GameSplash(State):
    """Game start state"""

    def __init__(self, *, machine):
        super().__init__(machine=machine)
        self.print_run = False

    def on_begin(self):
        print("on_begin called")

    def on_run(self):
        if not self.print_run:
            print("on_run called")
            self.print_run = True

    def on_exit(self):
        print("on_exit called")

class Game(StateMachine):
    """Game class"""

    def __init__(self, argv):
        super().__init__()
        self.window = pyglet.window.Window()
        self.window.on_draw = self.on_draw
        self.window.on_close = self.on_window_close

        #
        self.register_state('game_splash', GameSplash)

        #
        self.shutdown = False


    def on_window_close(self):
        self.shutdown = True

    def on_draw(self):
        self.window.clear()

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
            while not self.shutdown:
                #
                pyglet.clock.tick()

                #
                self.run_state()

                #
                for window in pyglet.app.windows:
                    window.switch_to()
                    window.dispatch_events()
                    window.dispatch_event('on_draw')
                    window.flip()

        except Exception as e:
            self._handle_except(e)

        finally:
            self.__cleanup()

        return 0

    def __cleanup(self):
        """House keeping after all's been done"""
        self.purge_stack()
