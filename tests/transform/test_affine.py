import pytest
import skbot.transform as rtf
import numpy as np


def test_1d_robot():
    arm = rtf.affine.Translation((1, 0))
    joint = rtf.affine.Rotation((1, 0), (0, 1))
    assert np.allclose(arm.direction, (1, 0))

    tool_frame = rtf.Frame(2)
    ellbow_frame = arm(tool_frame)
    world_frame = joint(ellbow_frame)

    joint.angle = 0
    tool_pos = tool_frame.transform((0, 0), to_frame=world_frame)
    assert np.allclose(tool_pos, (1, 0))

    joint.angle = np.pi / 2
    tool_pos = tool_frame.transform((0, 0), to_frame=world_frame)
    assert np.allclose(tool_pos, (0, -1))


def test_inverse_transform():
    frame1 = rtf.Frame(3)
    frame2 = rtf.affine.Translation((0, 1, 0))(frame1)

    result = frame1.transform((1, 0, 0), to_frame=frame2)
    assert np.allclose(result, (1, 1, 0))
    result = frame2.transform(result, to_frame=frame1)
    assert np.allclose(result, (1, 0, 0))


def test_matrix_identity():
    link = rtf.affine.Rotation((0, 1, 0), (0, 0, 1))

    world_frame = rtf.Frame(3)
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
    link = rtf.affine.Translation((1, 0))
    assert link.amount == 1

    frameA = rtf.Frame(2)
    frameB = link(frameA)

    point = np.array((0, 1), dtype=np.float_)
    point_in_B = np.array((1, 1), dtype=np.float_)
    assert np.allclose(frameA.transform(point, frameB), point_in_B)

    link.amount = 0
    assert np.allclose(frameA.transform(point, frameB), point)


def test_translation_direction():
    link = rtf.affine.Translation((1, 0))
    assert np.allclose(link.direction, (1, 0))

    link.direction = (0, 1)
    assert np.allclose(link.direction, (0, 1))


def test_affine_matrix():
    child = rtf.Frame(3)
    rotated = rtf.RotvecRotation((1, 0, 0), angle=0)(child)
    world = rtf.Translation((0, 1, 0))(rotated)

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
