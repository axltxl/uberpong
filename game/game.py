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
from docopt import docopt

from engine.state import State, StateMachine
from engine.spot import spot_set, spot_get

from game.states.splash import SplashState
from game.states.game import GameState

class Game(StateMachine):
    """Game class"""

    def __init__(self, argv):
        # Parse command line arguments
        self._parse_args(argv)

        # Parsed command line options
        self._options = spot_get('argv')

        # Populate SPOT with a bunch of defaults
        self._spot_init()

        #
        # Set up window
        #
        self._window = pyglet.window.Window(
            800, 600,
            style=pyglet.window.Window.WINDOW_STYLE_DIALOG,
            caption="{name} - {version}"
            .format(name=spot_get('game_name'),
                    version=spot_get('game_version'))
            )

        # pyglet.window basic callbacks
        self._window.on_draw = self.on_draw
        self._window.on_close = self.on_window_close

        # Call the parent
        super().__init__(window=self._window)

        # Register states
        self.register_state('state_splash', SplashState)
        self.register_state('state_game', GameState)

        # Shutdown flag
        self._shutdown = False

        # Register this object onto the SPOT
        spot_set('game_object', self)

        # Game-specific SPOT vars
        spot_set('paddle_position_start', (32, self._window.height // 2))
        spot_set('paddle_size', (32, 64))
        spot_set('ball_position_start', (self._window.width // 2, self._window.height // 2))
        spot_set('ball_size', (24, 24))

    def _spot_init(self):
        """Set initial SPOT values"""

        #
        # Common
        #
        spot_set('game_name', "PONG!")
        spot_set('game_version', "0.1a")

        # The server simulates the game in discrete time steps called ticks.
        # By default, the timestep is 15ms, so 66.666... ticks
        # per second are simulated
        spot_set('tickrate', 66)

        #
        # Client
        #

        # The rate at which a client sends requests to the server per second
        spot_set('cl_cmdrate', 30)

        # The client can request a certain snapshot rate
        spot_set('cl_updaterate', 20)

        #
        # Server
        #
        if self._options['--host'] is None:
            spot_set('sv_cheats', False)
            spot_set('sv_gravity', (0, 0))
            spot_set('sv_paddle_impulse', 3200)
            spot_set('sv_paddle_mass', 100)
            spot_set('sv_paddle_friction', 0.80)
            spot_set('sv_paddle_max_velocity', 1600)
            spot_set('sv_ball_mass', 10)
            spot_set('sv_ball_max_velocity', 800)

    def _parse_args(self, argv):
        """pong

        Usage:
            pong [-H <ip_address> | --host <ip_address>] [--port <port> | -p <port>] [--lz4 | -z]
            pong -h | --help
            pong --version

        Options:
          -z --lz4                    Use LZ4 compression algorithm
          -H --host <ip_address>      Server to connect to
          -p --port <port>            Port to connect to
          -h --help                   Show this screen.
          --version                   Show version.
        """
        spot_set("argv", docopt(self._parse_args.__doc__,
                 argv=argv, version=spot_get('game_version')))

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
