import pytest
import skbot.transform as tf
import numpy as np


def test_1d_robot():
    arm = tf.affine.Translation((1, 0))
    joint = tf.affine.Rotation((1, 0), (0, 1))
    assert np.allclose(arm.direction, (1, 0))

    tool_frame = tf.Frame(2)
    ellbow_frame = arm(tool_frame)
    world_frame = joint(ellbow_frame)

    joint.angle = 0
    tool_pos = tool_frame.transform((0, 0), to_frame=world_frame)
    assert np.allclose(tool_pos, (1, 0))

    joint.angle = np.pi / 2
    tool_pos = tool_frame.transform((0, 0), to_frame=world_frame)
    assert np.allclose(tool_pos, (0, -1))


def test_inverse_transform():
    frame1 = tf.Frame(3)
    frame2 = tf.affine.Translation((0, 1, 0))(frame1)

    result = frame1.transform((1, 0, 0), to_frame=frame2)
    assert np.allclose(result, (1, 1, 0))
    result = frame2.transform(result, to_frame=frame1)
    assert np.allclose(result, (1, 0, 0))


def test_matrix_identity():
    link = tf.affine.Rotation((0, 1, 0), (0, 0, 1))

    world_frame = tf.Frame(3)
    camera_frame = link(world_frame)

    link_mat = world_frame.get_affine_matrix(camera_frame)
    link_inv_mat = camera_frame.get_affine_matrix(world_frame)

    assert np.allclose(link_mat @ link_inv_mat, np.eye(4))
    assert np.allclose(link_inv_mat @ link_mat, np.eye(4))

    link.angle = np.pi / 2
    assert link.angle == np.pi / 2

    link_mat = world_frame.get_affine_matrix(camera_frame)
    link_inv_mat = camera_frame.get_affine_matrix(world_frame)

    assert np.allclose(link_mat @ link_inv_mat, np.eye(4))
    assert np.allclose(link_inv_mat @ link_mat, np.eye(4))


def test_translation_amount():
    link = tf.affine.Translation((1, 0))
    assert link.amount == 1

    frameA = tf.Frame(2)
    frameB = link(frameA)

    point = np.array((0, 1), dtype=np.float_)
    point_in_B = np.array((1, 1), dtype=np.float_)
    assert np.allclose(frameA.transform(point, frameB), point_in_B)

    link.amount = 0
    assert np.allclose(frameA.transform(point, frameB), point)


def test_translation_direction():
    link = tf.affine.Translation((1, 0))
    assert np.allclose(link.direction, (1, 0))

    link.direction = (0, 1)
    assert np.allclose(link.direction, (0, 1))


def test_affine_matrix():
    child = tf.Frame(3)
    rotated = tf.RotvecRotation((1, 0, 0), angle=0)(child)
    world = tf.Translation((0, 1, 0))(rotated)

    origin_in_world = child.transform((0, 0, 0), world)
    assert np.allclose(origin_in_world, (0, 1, 0))

    affine_matrix = child.get_affine_matrix(world)

    expected_tf = np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    assert np.allclose(affine_matrix, expected_tf)


def test_translation_dims():
    # this is a regression test (no GH issue filed)
    direction = np.array([[1, 2, 3]], dtype=np.float_)
    link = tf.Translation(direction)

    assert link.parent_dim == 3
    assert link.child_dim == 3


def test_affine():
    cartesian = tf.Frame(3)
    affine = tf.AffineSpace(3)(cartesian)

    input = np.array([[1, 0, 0], [1, 1, 0], [1, 1, 1]])
    expected = np.array([[1, 0, 0, 1], [1, 1, 0, 1], [1, 1, 1, 1]])

    as_affine = cartesian.transform(input, affine)
    assert np.allclose(as_affine, expected)

    as_cartesian = affine.transform(as_affine, cartesian)
    assert np.allclose(as_cartesian, input)

    input = np.array(
        [
            [1, 1, 1, 1],
            [0.5, 0.5, 0.5, 0.5],
            [3, 3, 3, 3],
            [0.1, 0.1, 0.1, 0.1],
        ]
    )
    expected = np.ones((4, 3))
    result = affine.transform(input, cartesian)
    assert np.allclose(result, expected)
