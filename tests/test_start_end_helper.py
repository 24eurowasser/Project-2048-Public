import numpy as np
from game2048.model import Model
from game2048.event_manager import EventManager
import pytest


@pytest.fixture()
def init():
    ev = EventManager()
    return Model(ev_manager=ev)


def test_empty_tiles_exist(init):

    # A completely full game field
    t1 = np.array([[2, 4, 8, 16], [4, 8, 16, 32], [8, 16, 32, 64], [16, 32, 64, 128]])
    init._field = t1
    assert (not init._empty_tiles_exist())

    # An empty game field
    t2 = np.zeros((4, 4))
    init._field = t1
    assert (not init._empty_tiles_exist())

    # A game field with only one empty tile
    t3 = np.array([[2, 4, 8, 16], [4, 8, 0, 32], [8, 16, 32, 64], [16, 32, 64, 128]])
    init._field = t3
    assert (init._empty_tiles_exist())
