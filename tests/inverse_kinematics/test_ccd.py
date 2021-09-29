from typing import List
import pytest
import skbot.inverse_kinematics as ik
import skbot.transform as tf
from typing import Union, List
import numpy as np


joint_types = Union[tf.RotationalJoint, tf.PrismaticJoint]


def test_panda(panda):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = panda
    tool_frame = base_frame.find_frame(".../panda_link8")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)
    expected = np.zeros(len(joints))

    for idx, joint in enumerate(joints):
        expected[idx] = joint.param
        joint.param = (joint.upper_limit - joint.lower_limit) / 2

    angles = ik.ccd((0, 0, 0), root_pos, tool_frame, base_frame, joints)
    final_pos = tool_frame.transform((0, 0, 0), base_frame)

    assert np.allclose(final_pos, root_pos, atol=0.001)
    # assert np.allclose(angles, expected)


def test_custom_distance(panda):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = panda
    tool_frame = base_frame.find_frame(".../panda_link8")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)
    expected = np.zeros(len(joints))

    for idx, joint in enumerate(joints):
        expected[idx] = joint.param
        joint.param = (joint.upper_limit - joint.lower_limit) / 2

    angles = ik.ccd(
        (0, 0, 0),
        root_pos,
        tool_frame,
        base_frame,
        joints,
        metric=lambda x, y: np.linalg.norm(x - y, ord=4),
    )
    final_pos = tool_frame.transform((0, 0, 0), base_frame)

    assert np.allclose(final_pos, root_pos, atol=0.001)
    # assert np.allclose(angles, expected)


def test_pendulum(double_pendulum):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = double_pendulum
    tool_frame = base_frame.find_frame(".../lower_link")

    for joint in joints:
        joint.param = (joint.upper_limit - joint.lower_limit) / 4

    root_pos = tool_frame.transform((0, 0, 0), base_frame)
    expected = np.zeros(len(joints))

    for idx, joint in enumerate(joints):
        expected[idx] = joint.param
        joint.param = (joint.upper_limit - joint.lower_limit) / 2

    angles = ik.ccd((0, 0, 0), root_pos, tool_frame, base_frame, joints)
    final_pos = tool_frame.transform((0, 0, 0), base_frame)

    assert np.allclose(final_pos, root_pos, atol=0.001)
    # assert np.allclose(angles, expected)


def test_ccd_maxiter(double_pendulum):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = double_pendulum
    tool_frame = base_frame.find_frame(".../lower_link")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)

    for joint in joints:
        joint.param = (joint.upper_limit - joint.lower_limit) / 2

    with pytest.raises(RuntimeError):
        ik.ccd((0, 0, 0), root_pos, tool_frame, base_frame, joints, maxiter=0)


def test_ccd_linesearch_maxiter(double_pendulum):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = double_pendulum
    tool_frame = base_frame.find_frame(".../lower_link")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)

    for joint in joints:
        joint.param = (joint.upper_limit - joint.lower_limit) / 2

    with pytest.raises(RuntimeError):
        ik.ccd(
            (0, 0, 0), root_pos, tool_frame, base_frame, joints, line_search_maxiter=1
        )
