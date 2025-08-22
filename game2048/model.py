"""This file implements the game logic behind 2048"""

import random
import pathlib
import os
import numpy as np
from .event_manager import (EventManager, SlideEvent, StateEvent, StartEvent)
from .arguments import (Command, Screen, Logging)
from .database import Database

db = Database()


class Model:
    """This class implements a model representation of the _game 2048.

    A gamefield is represented as a matrix of '_height' rows and
    '_width' columns. The components of the matrix represent either a tile
    with a specific value or is empty.
    Tiles can be moved and merged.

    Attributes
    ----------
    _field : np.ndarray
        Represents the actual _game _field with every tile.
    _highscore : int
        The current achieved high score.
    _height: int
        The _height of the _game _field.
    _width: int
        The _width of the _game _field.
    _ev_manager : EventManager
        controls communication with other modules
    """

    def __init__(self,
                 ev_manager: EventManager,
                 height=4,
                 width=4,
                 field=None):
        """Constructor of class Model.

        Parameters
        ----------
        height : int
            The number of rows.
        width : int
            The number of columns.
        field : np.ndarray
            A matrix representation of the _game.
        ev_manager : EventManager
            controls communication with other modules
        load : bool
            Indicate if we want to load a previous game
        """
        ## Load savestate
        # /.../project2048/2048/
        current_path = pathlib.Path(__file__).parent.resolve()
        # /.../project2048/
        project_path = current_path.parent
        # /.../project2048/database_content
        folder_name = "database_content"
        database_path = os.path.join(project_path, folder_name)
        # /.../project2048/database_content/Save... .json
        game_name = "Save - Game.json"
        record_name = "Save - Highscore.json"
        game_save_path = os.path.join(database_path, game_name)
        self.record_path = os.path.join(database_path, record_name)

        loaded_game = db.read_save(game_save_path)
        loaded_record = db.read_save(self.record_path)

        if field is None:
            self._height = height
            self._width = width
            self._field = np.zeros((self._height, self._width))
            self._start_game()
        else:
            self._field = field
            self._height = len(field)
            self._width = len(field[0])
        self._highscore = 0

        if loaded_game[0] is not False:
            self._highscore = loaded_game[0]
            self._field = loaded_game[1]

        if loaded_record[0] is False:
            self._record_highscore = 0
        else:
            self._record_highscore = loaded_record[0]

        self._ev_manager = ev_manager
        self._ev_manager.register_observer(self)


    def get_game(self) -> (np.ndarray, int, int):
        """Returns field, highscore and record highscore"""
        return self._field, self._highscore, self._record_highscore


    def notify(self, event: EventManager) -> None:
        """Handles incoming events

        Parameters
        ----------
        event: EventManager
            Specifies incoming event
        """
        if isinstance(event, SlideEvent):
            if event.data is Command.RESTART:
                self._restart()
            else:
                self._slide(event.data)


    def _start_game(self):
        """Adds the first two randomized tiles to the gamefield."""
        db.log(content="model.py -> _start_game was called.")
        tiles_required = 2

        while tiles_required > 0:
            self._add_tile()
            tiles_required -= 1


    def _restart(self) -> None:
        """Resets _field and _highscore to play again."""
        db.log(content="model.py -> _restart was called.")
        self.update_savestate()

        loaded_record = db.read_save(self.record_path)
        if loaded_record[0] is False:
            self._record_highscore = 0
        else:
            self._record_highscore = loaded_record[0]

        self._field = np.zeros((self._height, self._width))
        self._highscore = 0
        self._start_game()
        self._ev_manager.post(StateEvent(Screen.GAME))


    def _slide(self, command: Command) -> None:
        """Performs a slide action, based on a command from a controller class.

        Parameters
        ----------
        command : Command
            A command that determines the direction of slide action.
        """
        db.log(content="model.py -> _slide was called.")

        def rotation_nr(cmd: Command, reverse: bool) -> int:
            """Determines how many rotation (counter-clockwise) are necessary
            to turn the field, so that the direction of cmd is pointing
            to the left or to reverse the described rotation.

            Parameters
            ----------
            cmd: Command
                A command that determines the number of rotations.
            reverse : bool
                Indicates if the rotations process started (False)
                or if we want to go back to the original state (True)

            Returns
            -------
            int
                The number of rotations.
            """
            db.log(content="model.py -> rotation_nr was called.")
            if cmd is Command.LEFT:
                return 0
            if cmd is Command.RIGHT:
                return 2

            if reverse:
                if cmd is Command.DOWN:
                    return 1
                if cmd is Command.UP:
                    return 3
            else:
                if cmd is Command.DOWN:
                    return 3
                if cmd is Command.UP:
                    return 1

            raise Exception("Wrong command input for model.rotation_nr()")


        def move_tiles(field: np.ndarray) -> np.ndarray:
            """Moves the tiles in a field to the left.

            Attributes
            ----------
            field: np.ndarray
                A gamefield where all tiles should be moved to the left.

            Returns
            -------
            np.ndarray
                A gamefield, in which every tile were moved to the left.
            """
            db.log(content="model.py -> move_tiles was called.")

            width = len(field[0])
            height = len(field)

            for i in range(height):
                moved = [j for j in field[i] if j != 0]
                moved += [0 for _ in range(width - len(moved))]
                field[i] = moved
            return field


        def merge_tiles(field: np.ndarray) -> np.ndarray:
            """ Merges the tiles in a gamefield and
            updates the high score accordingly.

            Attributes
            ----------
            field: np.ndarray
                A gamefield, where all tiles should be merged to the left.

            Returns
            -------
            np.ndarray
                A gamefield – every possible merge to the left was executed.
            """
            db.log(content="model.py -> merge_tiles was called.")

            width = len(field[0])
            height = len(field)

            for i in range(height):
                for j in range(width - 1):
                    if field[i][j] == field[i][j + 1]:
                        field[i][j] *= 2
                        field[i][j + 1] = 0
                        self._update_highscore(field[i][j])

            return field

        cpy = np.copy(self._field)
        cpy = np.rot90(cpy, rotation_nr(command, False))
        cpy = move_tiles(cpy)
        cpy = merge_tiles(cpy)
        cpy = move_tiles(cpy)
        cpy = np.rot90(cpy, rotation_nr(command, True))

        db.log(content=cpy, option=Logging.GAMEFIELD)

        if not np.array_equal(self._field, cpy):
            self._field = cpy
            if self._empty_tiles_exist():
                self._add_tile()

        if self._check_losing(self._field):
            self._ev_manager.post(StateEvent(Screen.LOSE))
        if self._check_winning(self._field):
            self._ev_manager.post(StateEvent(Screen.WIN))


    def _update_highscore(self, add) -> None:
        """Updates the high score.

        Parameters
        ----------
        add : int
            The number of newly achieved points
        """
        db.log(content="model.py -> _update_highscore was called.")
        self._highscore += add


    def _add_tile(self) -> None:
        """Inserts either a new 2- or 4-tile randomly, in an empty tile."""
        db.log(content="model.py -> _add_tile was called.")
        for this_tile_pos in random.sample(self._update_empty_tiles(), k=1):
            # There is a 10% chance a tile 4 will be inserted, 90% of a 2
            if random.random() < 0.1:
                self._field[this_tile_pos] = 4
            else:
                self._field[this_tile_pos] = 2


    def _update_empty_tiles(self) -> list:
        """Returns a set of the current empty tiles in the gamefield.

        Returns
        -------
        Set
            The set of the current empty tiles.
        """
        db.log(content="model.py -> update_empty_tiles was called.")
        free_tiles = list(zip(*np.where(self._field == 0)))
        return free_tiles


    def _empty_tiles_exist(self) -> bool:
        """Indicates if there is still an empty tile left.

        Returns
        -------
        bool
            True, if we still have an empty tile in the gamefield.
        """
        db.log(content="model.py -> _empty_tiles_exist was called.")
        return len(self._update_empty_tiles()) > 0


    def _check_losing(self, field: np.ndarray) -> bool:
        """Checks if the player is still capable of playing the game
        in its current state. If not, then the player lost.

        Parameter
        ---------
        _field: np.ndarray
            A matrix of the current tiles in the game.

        Returns
        -------
        bool
            True, if the player lost the _game.
        """
        db.log(content="model.py -> _check_losing was called.")
        if self._empty_tiles_exist():
            return False

        # checks if matching tiles are next to each other
        width = len(field[0])
        height = len(field)
        tile = False
        for i in range(height):
            for j in range(width):
                if i < height-1 and field[i][j] == field[i+1][j]:
                    tile = True
                    break
                if j < width-1 and field[i][j] == field[i][j+1]:
                    tile = True
                    break

        return not tile


    @staticmethod
    def _check_winning(field: np.ndarray) -> bool:
        """Checks if the player won the game.

        Parameter
        ---------
        _field: np.ndarray
            A matrix of the current tiles in the game.

        Returns
        -------
        bool
            True, if the gamefield has a 2048-tile.
        """
        db.log(content="model.py -> _check_winning was called.")

        width = len(field[0])
        height = len(field)

        win = False
        for i in range(height):
            for j in range(width):
                if field[i][j] == 2048:
                    win = True
                    break
        return win


    def update_savestate(self) -> None:
        """Update the save file for the current gamefield and highscore"""
        db.create_save(matrix=self._field, current_highscore=self._highscore)
