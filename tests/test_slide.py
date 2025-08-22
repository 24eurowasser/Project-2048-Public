import pytest
import numpy as np
from game2048.model import Model
from game2048.event_manager import EventManager
from game2048.arguments import Command


def not_equal(curr, test):
    """Test if difference between fields can't occur because
    a random tile was inserted"""
    odd = -1
    for i in range(len(curr)):
        for j in range(len(curr[0])):
            if curr[i][j] != test[i][j] and odd > 0:
                return True
            else:
                if test[i][j] in [2, 4]:
                    odd = test[i][j]
                else:
                    return True
    return False


@pytest.fixture()
def init():
    ev = EventManager()
    return Model(ev_manager=ev)


def test_no_slide_merge_rot(init):
    old = np.array([[2, 4, 0, 0],
                    [8, 4, 2, 0],
                    [2, 4, 2, 0],
                    [16, 4, 2, 0]])
    init._field = old
    init._slide(Command.LEFT)
    assert np.array_equal(old, init._field)


def test_slide_merge_no_rot(init):
    old = np.array([[2, 4, 2, 2],
                    [4, 4, 2, 0],
                    [2, 4, 2, 0],
                    [4, 4, 2, 2]])
    new = np.array([[2, 4, 4, 0],
                    [8, 2, 0, 0],
                    [2, 4, 2, 0],
                    [8, 4, 0, 0]])
    init._field = old
    init._slide(Command.LEFT)
    assert not_equal(init._field, new)


def test_slide_merge_rot(init):
    old = np.array([[2, 4, 2, 2],
                    [4, 4, 2, 0],
                    [2, 4, 2, 0],
                    [4, 4, 0, 2]])
    new = np.array([[2, 0, 0, 0],
                    [4, 0, 0, 0],
                    [2, 8, 2, 0],
                    [4, 8, 4, 4]])
    init._field = old
    init._slide(Command.DOWN)
    assert not_equal(init._field, new)