import numpy as np
import pytest
from typing import List

import skbot.transform as tf


def test_missing_tf_matrix():
    link = tf.CustomLink(3, 3, lambda x: x)
    with pytest.raises(ValueError):
        link.invert()


def test_chain_resolution_dfs(simple_graph: List[tf.Frame]):
    # search order is not guaranteed
    cost = simple_graph[0].transform(0, simple_graph[7])
    assert cost == 5 or cost == 3

    # no path exists
    with pytest.raises(RuntimeError):
        simple_graph[1].transform((0), simple_graph[9])

    cost = simple_graph[0].transform(
        0, simple_graph[7], ignore_frames=[simple_graph[5]]
    )
    assert cost == 3


def test_chain_resolution_bfs(simple_graph: List[tf.Frame]):
    links = simple_graph[0].links_between(
        simple_graph[7], metric=tf.metrics.BreadthFirst
    )
    assert len(links) == 3

    # depends on which link is expanded first
    links = simple_graph[0].links_between(simple_graph[7], metric=tf.metrics.DepthFirst)
    assert len(links) == 3 or len(links) == 5


def test_transform_chain_max_depth(simple_graph: List[tf.Frame]):
    with pytest.raises(RuntimeError):
        simple_graph[0].links_between(simple_graph[7], max_depth=2)


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


def test_named_links_between():
    link = tf.Translation((1, 0))

    a = tf.Frame(2, name="foo")
    x = link(a)
    y = link(x)
    z = link(y)

    elements = z.links_between("foo")

    assert len(elements) == 3


def test_named_links_between():
    link = tf.Translation((1, 0))

    a = tf.Frame(2, name="foo")
    x = link(a)
    y = link(x)
    z = link(y)

    with pytest.deprecated_call():
        elements = z.transform_chain("foo")

    assert len(elements) == 3


def test_joints_between():
    joint1 = tf.RotationalJoint((0, 1, 0))
    joint2 = tf.PrismaticJoint((1, 0, 0))

    start = tf.Frame(3)
    x = tf.Rotation((1, 0, 0), (0, 1, 0))(start)
    x = tf.Translation((1, 0, 0))(x)
    x = joint1(x)
    x = tf.CompundLink(
        [joint2, tf.EulerRotation("xy", (90, -90), degrees=True), joint1]
    )(x)
    x = tf.Translation((1, 1, 0))(x)
    x = tf.Translation((1, 1, 1))(x)
    end = tf.InvertLink(joint2)(x)

    joints = start.joints_between(end)

    assert joints == [joint1, joint2, joint1, joint2]


def test_inverse_attributes():
    link = tf.Translation((1, 0), amount=0.5)
    inv_link = tf.InvertLink(link)

    hasattr(inv_link, "amount")
    assert inv_link.amount == 0.5


def test_inverse_inverse():
    link = tf.Translation((1, 0), amount=0.5)
    inv_link = tf.InvertLink(link)

    inverse_inverse = tf.InvertLink(inv_link)

    point = (3, 5)
    result = inverse_inverse.transform(point)
    expected = link.transform(point)

    assert np.allclose(result, expected)


def test_frames_between():
    link = tf.Translation((1, 0))

    a = tf.Frame(2, name="foo")
    x = link(a)
    y = link(x)
    z = link(y)

    elements = z.frames_between("foo")
    assert len(elements) == 4
    assert elements[0] == z
    assert elements[1] == y
    assert elements[2] == x
    assert elements[3] == a

    elements = z.frames_between("foo", include_self=False, include_to_frame=False)
    assert len(elements) == 2
    assert elements[0] == y
    assert elements[1] == x
