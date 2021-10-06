from typing import List
import pytest
import skbot.inverse_kinematics as ik
import skbot.transform as tf
import skbot.ignition as ign
from typing import List
import numpy as np
from skbot.inverse_kinematics.types import IKJoint as joint_types
from pathlib import Path


def test_panda(panda):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = panda
    tool_frame = base_frame.find_frame(".../panda_link8")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)
    expected = np.zeros(len(joints))

    for idx, joint in enumerate(joints):
        expected[idx] = joint.angle
        joint.angle = (joint.upper_limit + joint.lower_limit) / 2

    targets = [ik.PositionTarget((0, 0, 0), root_pos, tool_frame, base_frame)]
    angles = ik.ccd(targets, joints)
    final_pos = tool_frame.transform((0, 0, 0), base_frame)

    assert np.allclose(final_pos, root_pos, atol=0.001)
    # assert np.allclose(angles, expected)


def test_panda_orientation(panda):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = panda
    tool_frame = base_frame.find_frame(".../panda_link8")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)
    expected = np.zeros(len(joints))

    for idx, joint in enumerate(joints):
        expected[idx] = joint.param
        joint.param = (joint.upper_limit + joint.lower_limit) / 2

    targets = [
        ik.RotationTarget(
            tf.EulerRotation("Y", 90, degrees=True), tool_frame, base_frame
        )
    ]
    ik.ccd(targets, joints)

    tool_origin = tool_frame.transform((0, 0, 0), base_frame)
    tool_facing = tool_frame.transform((1, 0, 0), base_frame)
    final_ori = tool_facing - tool_origin

    assert np.allclose(final_ori, (0, 0, -1), atol=0.001)


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

    targets = [
        ik.PositionTarget(
            static_position=(0, 0, 0),
            dynamic_position=root_pos,
            static_frame=tool_frame,
            dynamic_frame=base_frame,
        )
    ]
    angles = ik.ccd(
        targets,
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
        joint.param = (joint.upper_limit + joint.lower_limit) / 4

    root_pos = tool_frame.transform((0, 0, 0), base_frame)
    expected = np.zeros(len(joints))

    for idx, joint in enumerate(joints):
        expected[idx] = joint.param
        joint.param = (joint.upper_limit + joint.lower_limit) / 2

    targets = [
        ik.PositionTarget(
            static_position=(0, 0, 0),
            dynamic_position=root_pos,
            static_frame=tool_frame,
            dynamic_frame=base_frame,
        )
    ]
    angles = ik.ccd(targets, joints)
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
        joint.param = (joint.upper_limit + joint.lower_limit) / 2

    targets = [ik.PositionTarget((0, 0, 0), root_pos, tool_frame, base_frame)]

    with pytest.raises(RuntimeError):
        ik.ccd(targets, joints, maxiter=0)


def test_ccd_linesearch_maxiter(panda):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = panda
    tool_frame = base_frame.find_frame(".../panda_link8")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)
    expected = np.zeros(len(joints))

    for idx, joint in enumerate(joints):
        expected[idx] = joint.param
        joint.param = (joint.upper_limit + joint.lower_limit) / 2

    targets = [
        ik.RotationTarget(
            tf.EulerRotation("Y", 90, degrees=True), tool_frame, base_frame
        )
    ]

    with pytest.raises(RuntimeError):
        ik.ccd(targets, joints, line_search_maxiter=1)


def test_multi_frame_ccd(panda):
    base_frame: tf.Frame
    joints: List[joint_types]
    base_frame, joints = panda
    tool_frame = base_frame.find_frame(".../panda_link8")

    root_pos = tool_frame.transform((0, 0, 0), base_frame)

    expected = np.zeros(len(joints))
    for idx, joint in enumerate(joints):
        expected[idx] = joint.angle
        joint.angle += 0.2

    targets = [
        ik.RotationTarget(
            tf.EulerRotation("X", 180, degrees=True), tool_frame, base_frame
        ),
        ik.PositionTarget((0, 0, 0), root_pos, tool_frame, base_frame),
    ]

    ik.ccd(targets, joints, atol=0.01)

    tool_origin = tool_frame.transform((0, 0, 0), base_frame)
    tool_facing = tool_frame.transform((0, 0, 1), base_frame)
    final_ori = tool_facing - tool_origin
    assert np.allclose(final_ori, (0, 0, -1), atol=0.001)

    final_pos = tool_frame.transform((0, 0, 0), base_frame)
    assert np.allclose(final_pos, root_pos, atol=0.001)


def test_camera_steering():
    model_file = (
        Path(__file__).parents[1] / "ignition" / "sdf" / "v18" / "panda_cam.sdf"
    )
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    frames = world_sdf.declared_frames()
    world_sdf.to_dynamic_graph(frames)

    world_frame = frames["world"]
    px_space = frames["camera_model::camera_link::camera_sensor::pixel_space"]
    base_frame = frames["panda::panda_link0"]
    tool_frame = frames["panda::panda_link8"]

    joints = list()
    for link in tool_frame.links_between(base_frame):
        if isinstance(link, (tf.RotationalJoint, tf.PrismaticJoint)):
            joints.append(link)

    for value, joint in zip([0, -0.785, 0, -2.356, 0, 1.571, 0.785], reversed(joints)):
        joint.angle = value

    targets = [ik.PositionTarget((0, 0, 0), (1920 / 3, 1080 / 3), tool_frame, px_space)]
    ik.ccd(targets, joints)

    for target in targets:
        assert target.score() < target.atol

    result_pos = targets[0].static_frame.transform(
        targets[0].static_position, targets[0].dynamic_frame
    )
    target_pos = targets[0].dynamic_position

    assert np.allclose(result_pos, target_pos, 0.001)
