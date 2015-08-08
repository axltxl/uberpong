# -*- coding: utf-8 -*-

import pyglet

class Game:
    """Game class"""
    def __init__(self, argv):
        self.window = pyglet.window.Window()
        self.window.on_draw = self.on_draw

    def on_draw(self):
        self.window.clear()

    def go(self):
        """Main entry point"""
        try:
            pyglet.app.run()
        except:
            pass
        finally:
            self.__cleanup()
        return 0

    def __cleanup(self):
        """House keeping after all's been done"""
        pass
