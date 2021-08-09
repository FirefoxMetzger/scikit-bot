import pytest

import skbot.transform as tf


@pytest.fixture()
def simple_graph():
    frames = [tf.Frame(1, name=f"frame{str(idx)}") for idx in range(10)]

    def directional(idxA, idxB):
        # "degenerate" links that track path cost
        tf.CustomLink(1, 1, lambda x: x + 1)(
            frames[idxA], frames[idxB], add_inverse=False
        )

    def undirectional(idxA, idxB):
        tf.CustomLink(1, 1, lambda x: x + 1)(frames[idxA], frames[idxB])
        tf.CustomLink(1, 1, lambda x: x + 1)(frames[idxB], frames[idxA])

    undirectional(0, 2)
    undirectional(3, 2)
    undirectional(4, 2)
    undirectional(6, 2)
    undirectional(4, 5)
    undirectional(5, 9)
    undirectional(5, 6)
    undirectional(6, 8)

    directional(6, 7)
    directional(2, 1)
    directional(5, 8)

    return frames
