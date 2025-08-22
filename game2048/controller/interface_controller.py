"""This file implements the abstract controller class"""

from abc import ABC, abstractmethod
import pygame
import curses
from ..event_manager import (EventManager, InputRequest, StateEvent,
                             SlideEvent, QuitEvent, Event)
from ..arguments import (Screen, Command)
from ..database import Database

db = Database()


class InterfaceController(ABC):
    """Interface for the Controller module of the 2048 game."""
    @abstractmethod
    def __init__(self, ev_manager: EventManager):
        """Constructor of the class ControllerLocal.

        Parameters:
        ----------
        _ev_manager: EventManager
            controls communication with other modules
        _screen: curses.window
            the shell screen or None for GUI view
        """
        self._game_state = Screen.INSTRUCTIONS
        self._ev_manager = ev_manager
        ev_manager.register_observer(self)

    def notify(self, event: Event):
        """Handles incoming events

        Parameters
        ----------
        event: EventManager
            Specifies incoming event
        """
        if isinstance(event, StateEvent):
            self._game_state = event.data

    def translate_command(self, command: Command) -> Event:
        """Verify input with the current game state and return matching event

        Parameters
        ----------
        command: Command
            A command to play the game

        Returns
        -------
        Event
            Matching game event
        None
            If command is not possible return None implicitly
        """
        if self._game_state == Screen.GAME:
            if command in [Command.UP, Command.DOWN, Command.RIGHT, Command.LEFT]:
                return SlideEvent(command)
            if command == Command.PAUSE:
                return StateEvent(Screen.PAUSE)
        else:
            if command == Command.EXIT:
                db.log(content="End the game", final_log=True)
                return QuitEvent()
            if command == Command.START:
                if self._game_state in [Screen.WIN, Screen.LOSE]:
                    return SlideEvent(Command.RESTART)
                return StateEvent(Screen.GAME)
            if command == Command.RESTART and self._game_state == Screen.PAUSE:
                return SlideEvent(command)

    def _play_the_game(self, command: Command):
        """Execute a command if possible in the current game state"""
        event = self.translate_command(command)
        if event is not None:
            self._ev_manager.post(event)
