from game2048.model import Model
from game2048.event_manager import EventManager
import numpy as np
import pytest


@pytest.fixture()
def init():
    ev = EventManager()
    return Model(ev_manager=ev)


def test_check_losing(init):
    # Full game field with no matching tiles next to each other
    f1 = np.array([[2,  4,   8,  16],
                   [4,  8,  16,  32],
                   [8,  16, 32,  64],
                   [16, 32, 64, 128]])
    init._field = f1
    assert (init._check_losing(f1))

    # Full game field, but with two matching tiles next to each other
    f2 = np.array([[2, 4, 8, 16], [4, 8, 16, 32], [8, 16, 32, 128], [16, 32, 64, 128]])
    init._field = f2
    assert (not init._check_losing(f2))

    # A game field that is not full
    f3 = np.array([[2, 4, 8, 16], [4, 8, 0, 32], [8, 16, 32, 64], [16, 32, 64, 128]])
    init._field = f3
    assert (not init._check_losing(f3))


def test_check_winning(init):
    f1 = np.array([[2, 4, 8, 16], [4, 8, 16, 32], [8, 16, 32, 64], [16, 32, 64, 128]])
    f2 = np.array([[2, 4, 8, 16], [4, 8, 16, 32], [8, 16, 32, 64], [16, 32, 2048, 128]])

    assert (not init._check_winning(f1) and init._check_winning(f2))
