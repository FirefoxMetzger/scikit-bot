import numpy as np
import ropy.transform as rtf
import pytest


def test_missing_tf_matrix():
    world_frame = rtf.Frame(3)
    camera_frame = rtf.Frame(3)

    link = rtf.affine.Fixed(world_frame, camera_frame, lambda x: x)

    with pytest.raises(ValueError):
        rtf.affine.Inverse(link)


def test_chain_resolution():
    frames = [rtf.Frame(1) for _ in range(10)]

    def directional(idxA, idxB):
        # "degenerate" links that track path cost
        link = rtf.affine.Fixed(frames[idxA], frames[idxB], lambda x: x + 1)
        frames[idxA].add_link(link)

    def undirectional(idxA, idxB):
        directional(idxA, idxB)
        directional(idxB, idxA)

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


def test_invalid_parent():
    frames = [rtf.Frame(1) for _ in range(2)]

    link = rtf.affine.Fixed(frames[0], frames[1], lambda x: x)
    
    with pytest.raises(ValueError):
        frames[1].add_link(link)