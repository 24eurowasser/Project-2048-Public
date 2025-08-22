"""This file implements the Shell output of 2048"""

import curses
import time
import numpy as np
from .interface_view import InterfaceView
from ..event_manager import EventManager
from ..arguments import Screen
from ..model import Model
from ..database import Database

db = Database()


class ViewShell(InterfaceView):
    """This class implements a shell output of the game 2048"""

    def __init__(self, ev_manager: EventManager, game: Model, screen: curses.window):
        """Constructs the shell output window

        Parameters
        ----------
        ev_manager: EventManager
            controls communication with other modules
        game: Model
            Reference to the model instance
        screen: curses.window
            the shell output screen
        """
        super().__init__(ev_manager, game)

        self._screen = screen
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        curses.curs_set(False)
        screen.nodelay(True)


    def _quit(self, field: np.ndarray, highscore: int) -> None:
        """Ends the game"""
        db.create_save(matrix=field, current_highscore=highscore)
        self._screen.clear()
        self._screen.addstr(1, 7, "EXIT", curses.A_STANDOUT)
        self._screen.addstr(3, 0, "Good Bye! Thank you for playing!")
        self._screen.addstr(4, 0, "Come back soon <3")
        self._screen.addstr(6, 0, "Your highscore: " + str(highscore), curses.A_STANDOUT)
        self._screen.refresh()

        time.sleep(3)
        curses.nocbreak()
        self._screen.keypad(False)
        curses.echo()
        curses.curs_set(True)
        curses.endwin()

    def _print_pause(self) -> None:
        """Displays the pause screen"""
        self._screen.clear()
        self._screen.addstr(1, 7, "PAUSE", curses.A_STANDOUT)
        self._screen.addstr(2, 1, "Press:")
        self._screen.addstr(3, 0, " s to continue  |  r to restart  |  q to exit")
        self._screen.refresh()

    def _print_instructions(self) -> None:
        """Displays a welcome message and instructions for players."""
        self._screen.clear()
        self._screen.addstr(1, 7, "WELCOME TO 2048!", curses.A_STANDOUT)
        self._screen.addstr(3, 0, "Your aim in this game is to reach a value of")
        self._screen.addstr(4, 0, "2048 on one of the tiles by merging the appropriate tiles!")
        self._screen.addstr(5, 0, "You should do so by cleverly sliding them ( ← | ↑ | → | ↓ )")
        self._screen.addstr(6, 0, "Be careful when sliding:")
        self._screen.addstr(7, 0, "you slide ALL the tiles in that direction, not just one :)")
        self._screen.addstr(8, 0, "Good luck!")
        self._screen.addstr(10, 0, " s ~ start game  |  q ~ exit")
        self._screen.refresh()

    def _print_final(self, score: int, record: int) -> None:
        """Displays the ending screen & the reason why game has ended.

        Parameters
        ----------
        score: int
            The current high score.
        """
        self._screen.clear()
        if self._game_state is Screen.WIN:
            self._screen.addstr(1, 7, "CONGRATULATIONS!", curses.A_STANDOUT)
            self._screen.addstr(3, 0, "You reached a 2048 tile and WON!")
            self._screen.addstr(4, 0, "Your Final Score: " + str(int(score)))
            self._screen.addstr(5, 0, "The Current Record: " + str(int(record)))
            self._screen.addstr(7, 0, "s ~ start new game  |  q ~ quit")

        if self._game_state is Screen.LOSE:
            self._screen.addstr(1, 7, "!!! GAME OVER !!!", curses.A_STANDOUT)
            self._screen.addstr(3, 0, "You lost!")
            self._screen.addstr(4, 0, "Your Final Score: " + str(int(score)))
            self._screen.addstr(5, 0, "The Current Record: " + str(int(record)))
            self._screen.addstr(6, 0, "Better luck next time! ;)")
            self._screen.addstr(7, 0, "s ~ start new game  |  q ~ quit")
        self._screen.refresh()

    def _print_game(self, matrix: np.ndarray, score: int, record: int) -> None:
        """Displays a given matrix and high score in the shell.

        Parameter
        ---------
        matrix: np.ndarray
            The current gamefield.
        score: int
            The current high score.
        """
        def max_tile() -> int:
            """Returns max number of decimal places in all fields of matrix"""
            max_elem: int = 0
            for i in matrix:
                for j in i:
                    if int(j) > max_elem:
                        max_elem = int(j)

            return max_elem

        def tile_string() -> str:
            """Return output string for a tile with correct number of empty spaces"""
            tile_len: int = len(str(int(tile)))
            spaces_r = int((tile_width - tile_len) / 2)
            spaces_l = tile_width - tile_len - spaces_r

            if int(tile) == 0:
                return tile_width * ' ' + '|'

            return spaces_l * ' ' + str(int(tile)) + spaces_r * ' ' + '|'

        width = len(matrix[0])                          # Calculates the needed width with the help of max_tile
        tile_width = len(str(int(max_tile()))) + 4      #  so that all tile widths adjust to the biggest number 
                                                        #  on the field
        self._screen.clear()
        self._screen.addstr(1, 7, 'Current Score: ' + str(int(score)), curses.A_STANDOUT)
        self._screen.addstr(2, 7, 'Current Record: ' + str(int(record)), curses.A_STANDOUT)

        self._screen.addstr(3, 3, width * (' ' + tile_width * '_') + '\n')

        for idx, row in enumerate(matrix):
            self._screen.addstr(4 + idx * 3, 3, width * ('|' + tile_width * ' ') + '|' + '\n')

            line = '|'
            for tile in row:
                line += tile_string()

            self._screen.addstr(5 + idx * 3, 3, line)
            self._screen.addstr(6 + idx * 3, 3, width * ('|' + tile_width * '_') + '|' + '\n')

        self._screen.addstr(17, 0, "Use arrow keys  ← / ↑ / → / ↓ ~ slide  |  p ~ pause")

        self._screen.refresh()
