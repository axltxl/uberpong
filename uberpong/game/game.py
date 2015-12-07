# -*- coding: utf-8 -*-

"""
game.game
~~~~~~~~
Game main entry point

(c) 2015 by Alejandro Ricoveri
See LICENSE for more details.
"""


import traceback
import os
import sys
import pyglet

from docopt import docopt
from os import path
from uberpong.engine.state import State, StateMachine
from uberpong.engine.spot import spot_set, spot_get
from uberpong.engine.sorcerer import Sorcerer
from uberpong import (
    __name__ as pkg_name,
    __author__ as pkg_author,
    __version__ as pkg_version,
)

from .net import PlayerClient, Scene

from .states import (
    CreditsState,
    SplashState,
    RoundState,
    LoadState,
    BeginState,
    ScoreState,
    GameSetState,
    WaitState
)


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
        self.register_state('game_credits', CreditsState)
        self.register_state('game_splash', SplashState)
        self.register_state('game_round', RoundState)
        self.register_state('game_load', LoadState)
        self.register_state('game_begin', BeginState)
        self.register_state('game_wait', WaitState)
        self.register_state('game_score', ScoreState)
        self.register_state('game_set', GameSetState)

        # Shutdown flag
        self._shutdown = False

        # Register this object onto the SPOT
        spot_set('game_object', self)

        # Game-specific SPOT vars
        spot_set('paddle_position_start', (32, self._window.height // 2))
        spot_set('paddle_size', (32, 64))
        spot_set(
            'ball_position_start',
            (self._window.width // 2, self._window.height // 2)
        )
        spot_set('ball_size', (32, 32))
        spot_set(
            'cl_scores_position',
            (self._window.width // 2, self._window.height - 32)
        )

        ########################################
        # assets will be looked up at sys.prefix
        # by default, that is unless ASPATH environment
        # variable has been specified
        ########################################
        assets_path = os.getenv('ASPATH')
        if assets_path is None:
            assets_path = path.join(sys.prefix,
                                    'share/{}/assets'.format(pkg_name))

        # sourcerer a.k.a. resource manager
        self._sorcerer = Sorcerer(root_dir=path.join(assets_path))

        #
        # Create server and client
        #
        self._client = None
        self._server = None
        self.create_client(self.create_server())

    def _spot_init(self):
        """Set initial SPOT values"""

        #
        # Common
        #
        spot_set('game_name', "Uber Pong!")
        spot_set('game_version', pkg_version)

        # Network protocol codec to be used
        spot_set('net_codec', 'json')

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
            spot_set('sv_score_max', 10)

        # Default server port for either server or client
        spot_set('sv_port', int(self._options['--port']))

    def _parse_args(self, argv):
        """pong

        Usage:
            pong [-H <ip_address> | --host <ip_address>] [--port <port> | -p <port>] [--lz4 | -z]
            pong -h | --help
            pong --version

        Options:
          -z --lz4                    Use LZ4 compression algorithm
          -H --host <ip_address>      Server to connect to
          -p --port <port>            Port to connect to [default: 54212]
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

    def create_server(self):
        """Create the server"""

        #
        # Get argv parsed options
        #
        options = spot_get('argv')

        #
        # Initialise server
        #
        if options['--host'] is None:

            # set server address
            server_addr = 'localhost'

            # Create the actual server
            self._server = Scene(port=spot_get('sv_port'),
                                 width=self._window.width,
                                 height=self._window.height,
                                 codec=spot_get('net_codec'))

            # Activate LZ4 compression on client
            if options['--lz4']:
                self._server.use_lz4 = True

            # Set it on SPOT
            spot_set('game_server', self._server)

        else:
            server_addr = options["--host"]

        # return server address
        return server_addr

    def create_client(self, server_addr):
        """Create the client"""

        #
        # Get argv parsed options
        #
        options = spot_get('argv')

        #
        # Create client
        #
        self._client = PlayerClient(
            window=self._window,
            ball_position=spot_get('ball_position_start'),
            address=server_addr,
            port=spot_get('sv_port'),
            codec=spot_get('net_codec')
        )

        #
        # Activate LZ4 compression on client
        #
        if options['--lz4']:
            self._client.use_lz4 = True

        # Set it on SPOT
        spot_set('game_client', self._client)

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
            self.push_state('game_credits')

            # Run the thing!
            while not self._shutdown:
                #
                pyglet.clock.tick()

                # Pump network traffic on client
                if self._client is not None:
                    self._client.pump()

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

        # Client disconnection
        if self._client is not None:
            self._client.disconnect()
            self._client.close()

        # Scene server disconnection
        if self._server is not None:
            self._server.close()

        # TODO: document this
        self.purge_stack()

    @property
    def sorcerer(self):
        return self._sorcerer
