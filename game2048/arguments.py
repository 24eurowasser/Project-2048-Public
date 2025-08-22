"""This file implements the global command enums"""

from enum import Enum


class Command(Enum):
    """Commands that are updating the model."""
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    RESTART = 5
    EXIT = 6
    PAUSE = 7
    START = 8
    EMPTY = 9


class Screen(Enum):
    """Possible game screens."""
    INSTRUCTIONS = 1
    GAME = 2
    PAUSE = 3
    WIN = 4
    LOSE = 5


class Logging(Enum):
    """Possible logging options."""
    COMMENT = 1
    USER_INPUT = 2
    COMMAND = 3
    GAMEFIELD = 4