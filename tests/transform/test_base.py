import numpy as np
import skbot.transform as tf
import pytest


def test_missing_tf_matrix():
    link = tf.CustomLink(3, 3, lambda x: x)
    with pytest.raises(ValueError):
        link.invert()


def test_chain_resolution(simple_graph):
    # DFS finds sub-optial chains
    cost = simple_graph[0].transform(0, simple_graph[7])
    assert cost == 5

    # no path exists
    with pytest.raises(RuntimeError):
        simple_graph[1].transform((0), simple_graph[9])

    cost = simple_graph[0].transform(
        0, simple_graph[7], ignore_frames=[simple_graph[5]]
    )
    assert cost == 3


def test_find_frame(simple_graph):

    start: tf.Frame = simple_graph[0]
    frame_seven = start.find_frame(".../frame7")
    assert frame_seven == simple_graph[7]

    frame_seven = start.find_frame("frame0/frame2/frame6/frame5")
    assert frame_seven == simple_graph[5]

    # no path exists
    start = simple_graph[1]
    with pytest.raises(RuntimeError):
        start.find_frame(".../frame9")
    with pytest.raises(ValueError):
        start.find_frame(".../...")

    # failes because path doesn't start at frame1
    start = simple_graph[4]
    with pytest.raises(RuntimeError):
        start.find_frame("frame1/.../frame5")


@pytest.mark.parametrize(
    "vec_child, vec_parent",
    [
        ((0, 0, 0), (3, 1, 3)),
        ((2, 0, 0), (3, 3, 3)),
        ((0, 1, 0), (2, 1, 3)),
    ],
)
def test_compound_frame(vec_child, vec_parent):
    translation = tf.Translation((3, 1, 3))
    rotation = tf.EulerRotation("Z", 90, degrees=True)

    pose = tf.CompundLink([rotation, translation])

    out = pose.transform(vec_child)
    assert np.allclose(out, vec_parent)

    out = pose.__inverse_transform__(vec_parent)
    assert np.allclose(out, vec_child)
