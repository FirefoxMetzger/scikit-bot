from typing import List
import pytest
import skbot.inverse_kinematics as ik
import skbot.transform as tf
from typing import Union, List
import numpy as np

from skbot.transform.utils3d import EulerRotation


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
        joint.param = joint.param + 0.2

    targets = [ik.PositionTarget((0, 0, 0), root_pos, tool_frame, base_frame)]
    angles = ik.gd(targets, joints)
    final_pos = tool_frame.transform((0, 0, 0), base_frame)

    assert np.allclose(final_pos, root_pos, atol=0.001)


def test_panda_orientation(panda):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = panda
    tool_frame = base_frame.find_frame(".../panda_link8")

    expected = np.zeros(len(joints))
    for idx, joint in enumerate(joints):
        expected[idx] = joint.param
        joint.param = joint.param + 0.2

    targets = [
        ik.RotationTarget(
            tf.EulerRotation("Y", 90, degrees=True), tool_frame, base_frame
        )
    ]
    ik.gd(targets, joints)

    tool_origin = tool_frame.transform((0, 0, 0), base_frame)
    tool_facing = tool_frame.transform((1, 0, 0), base_frame)
    final_ori = tool_facing - tool_origin

    assert np.allclose(final_ori, (0, 0, -1), atol=0.001)


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

    targets = [
        ik.PositionTarget(
            static_position=(0, 0, 0),
            dynamic_position=root_pos,
            static_frame=tool_frame,
            dynamic_frame=base_frame,
        )
    ]
    angles = ik.gd(targets, joints)
    final_pos = tool_frame.transform((0, 0, 0), base_frame)

    assert np.allclose(final_pos, root_pos, atol=0.001)


def test_maxiter(double_pendulum):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = double_pendulum
    tool_frame = base_frame.find_frame(".../lower_link")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)

    for joint in joints:
        joint.param = (joint.upper_limit - joint.lower_limit) / 2

    targets = [ik.PositionTarget((0, 0, 0), root_pos, tool_frame, base_frame)]

    with pytest.raises(RuntimeError):
        ik.gd(targets, joints, maxiter=0)


def test_multi_frame_ccd(panda):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = panda
    tool_frame = base_frame.find_frame(".../panda_link8")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)

    tool_origin = tool_frame.transform((0, 0, 0), base_frame)
    tool_facing = tool_frame.transform((0, 1, 0), base_frame)
    initial_ori = tool_facing - tool_origin

    expected = np.zeros(len(joints))
    for idx, joint in enumerate(joints):
        expected[idx] = joint.param
        joint.param += 0.2

    targets = [
        ik.PositionTarget((0, 0, 0), root_pos, tool_frame, base_frame),
        ik.RotationTarget(
            tf.EulerRotation("X", 180, degrees=True), tool_frame, base_frame
        ),
    ]

    ik.gd(targets, joints)

    tool_origin = tool_frame.transform((0, 0, 0), base_frame)
    tool_facing = tool_frame.transform((0, 0, 1), base_frame)
    final_ori = tool_facing - tool_origin
    assert np.allclose(final_ori, (0, 0, -1), atol=0.001)

    final_pos = tool_frame.transform((0, 0, 0), base_frame)
    assert np.allclose(final_pos, root_pos, atol=0.001)
