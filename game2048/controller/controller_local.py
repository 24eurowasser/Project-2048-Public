"""This file implements the local keyboard input decoding"""

import curses
from .interface_controller import InterfaceController
from ..event_manager import EventManager, InputRequest, Event
from ..arguments import Command
import pygame


class ControllerLocal(InterfaceController):
    """This class implements the keyboard as input source to play 2048."""
    def __init__(self, ev_manager: EventManager, screen: curses.window):
        """
        Constructor of the class ControllerLocal.

        Parameters:
        ----------
        _ev_manager: EventManager
            controls communication with other modules
        _screen: curses.window
            the shell screen or None for GUI view
        """
        super().__init__(ev_manager)

        self._screen = screen

    def notify(self, event: Event):
        """Handles incoming events

        Parameters
        ----------
        event: EventManager
            Specifies incoming event
        """
        super().notify(event)

        if isinstance(event, InputRequest):
            self._get_input()

    def _get_input(self) -> None:
        """Decodes Keyboard input and triggers the events"""
        def get_input_pygame() -> Command:
            """Gets input from GUI"""
            inp = pygame.event.poll()
            if inp.type == pygame.QUIT:
                return Command.EXIT
            if inp.type == pygame.KEYDOWN:
                if inp.key == pygame.K_RIGHT:
                    return Command.RIGHT
                if inp.key == pygame.K_LEFT:
                    return Command.LEFT
                if inp.key == pygame.K_UP:
                    return Command.UP
                if inp.key == pygame.K_DOWN:
                    return Command.DOWN
                if inp.key == pygame.K_p:
                    return Command.PAUSE
                if inp.key == pygame.K_q:
                    return Command.EXIT
                if inp.key == pygame.K_r:
                    return Command.RESTART
                if inp.key == pygame.K_s:
                    return Command.START

        def get_input_curses() -> Command:
            """Gets input from shell"""
            inp = self._screen.getch()
            if inp == curses.KEY_RIGHT:
                return Command.RIGHT
            if inp == curses.KEY_LEFT:
                return Command.LEFT
            if inp == curses.KEY_UP:
                return Command.UP
            if inp == curses.KEY_DOWN:
                return Command.DOWN
            if inp == ord('p'):
                return Command.PAUSE
            if inp == ord('q'):
                return Command.EXIT
            if inp == ord('r'):
                return Command.RESTART
            if inp == ord('s'):
                return Command.START

        cmd = get_input_pygame() if self._screen is None else get_input_curses()
        self._play_the_game(cmd)
