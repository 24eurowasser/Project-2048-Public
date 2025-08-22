"""This file implements the abstract view class"""

from abc import ABC, abstractmethod
import time
import numpy as np
from ..event_manager import Event, StateEvent, QuitEvent, StartEvent, InputRequest, EventManager
from ..model import Model
from ..arguments import Screen
from ..database import Database

db = Database()


class InterfaceView(ABC):
    """Implements the view of our 2048 game."""

    def __init__(self, ev_manager: EventManager, game: Model):
        """Constructs the shell output window

        Parameters
        ----------
        ev_manager: EventManager
            controls communication with other modules
        game: Model
            Reference to the model instance
        """
        ev_manager.register_observer(self)
        self._ev_manager = ev_manager
        self._game_state = Screen.INSTRUCTIONS
        self._game = game
        self._running = True
        self._fps = 60

    def notify(self, event: Event) -> None:
        """
        Handles incoming events

        Parameters
        ----------
        event: EventManager
            Specifies incoming event
        """
        if isinstance(event, QuitEvent):
            self._running = False
            content = self._game.get_game()
            self._quit(field=content[0], highscore=content[2])
        if isinstance(event, StateEvent):
            self._game_state = event.data
        if isinstance(event, StartEvent):
            self._run()

    def _draw(self) -> None:
        """Outputs the current Screen"""
        if self._game_state == Screen.INSTRUCTIONS:
            self._print_instructions()
        elif self._game_state == Screen.GAME:
            self._print_game(self._game.get_game()[0], self._game.get_game()[1], self._game.get_game()[2])
        elif self._game_state == Screen.PAUSE:
            self._print_pause()
        else:
            self._print_final(self._game.get_game()[1], self._game.get_game()[2])

    def _run(self) -> None:
        """Main game loop runs with fps speed"""
        db.log(content="interface_view.py -> _run was called.")
        while self._running:
            end = time.time() + 1.0 / self._fps

            self._draw()

            time.sleep(max([0, end - time.time()]))
            self._ev_manager.post(InputRequest())
        # wait for the endscreen (main thread terminates here)
        time.sleep(3)

    @abstractmethod
    def _quit(self, field: np.ndarray, highscore: int):
        pass

    @abstractmethod
    def _print_instructions(self):
        pass

    @abstractmethod
    def _print_pause(self):
        pass

    @abstractmethod
    def _print_game(self, field, score, record):
        pass

    @abstractmethod
    def _print_final(self, score, record):
        pass
