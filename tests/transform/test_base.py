import numpy as np
import skbot.transform as rtf
import pytest


def test_missing_tf_matrix():
    link = rtf.CustomLink(3, 3, lambda x: x)
    with pytest.raises(ValueError):
        link.invert()


def test_chain_resolution():
    frames = [rtf.Frame(1) for _ in range(10)]

    def directional(idxA, idxB):
        # "degenerate" links that track path cost
        rtf.CustomLink(1, 1, lambda x: x + 1)(
            frames[idxA], frames[idxB], add_inverse=False
        )

    def undirectional(idxA, idxB):
        rtf.CustomLink(1, 1, lambda x: x + 1)(frames[idxA], frames[idxB])
        rtf.CustomLink(1, 1, lambda x: x + 1)(frames[idxB], frames[idxA])

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

    # DFS finds sub-optial chains
    cost = frames[0].transform(0, frames[7])
    assert cost == 5

    # no path exists
    with pytest.raises(RuntimeError):
        frames[1].transform((0), frames[9])

    cost = frames[0].transform(0, frames[7], ignore_frames=[frames[5]])
    assert cost == 3
