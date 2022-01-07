import pytest
import skbot.inverse_kinematics as ik
import skbot.transform as tf
from typing import List
import numpy as np


def test_target():
    frameA = tf.Frame(2, name="root")
    joint = tf.PrismaticJoint((1, 0), upper_limit=10, lower_limit=-10)
    frameB = joint(frameA)

    target = ik.Target(frameB, frameA)
    assert target.uses(joint)
    assert target.usage_count(joint) == 1

    missing_joint = tf.PrismaticJoint((1, 0), upper_limit=2, lower_limit=-2)
    assert target.uses(missing_joint) == False
    assert target.usage_count(missing_joint) == 0

    target = ik.Target(frameA, frameB)
    assert target.uses(joint)
    assert target.usage_count(joint) == 1


def test_position_target(circle_bot):
    world: tf.Frame
    joints: List[tf.Link]

    world, joints = circle_bot
    tool = world.find_frame("world/ellbow/tool")

    target = ik.PositionTarget(
        (0, 0, 0), (5, 0, 0), tool, world, norm=lambda x: np.linalg.norm(x, axis=-1)
    )
    assert target.score() == 4

    plane_project = tf.CustomLink(3, 2, lambda x: x[..., :2])
    plane = plane_project(world)
    target = ik.PositionTarget((0, 0, 0), (2, 0), tool, plane)

    assert target.score() == 1


def test_rotation_target(circle_bot):
    world: tf.Frame
    joints: List[tf.Link]

    world, joints = circle_bot
    tool = world.find_frame("world/ellbow/tool")

    target = ik.RotationTarget(
        tf.RotvecRotation((0, 0, 1), angle=45, degrees=True),
        tool,
        world,
    )
    assert np.isclose(target.score(), np.pi / 4)

    target = ik.RotationTarget(
        [
            tf.RotvecRotation((0, 0, 1), angle=45, degrees=True),
            tf.RotvecRotation((0, 0, 1), angle=45, degrees=True),
        ],
        tool,
        world,
    )
    assert np.isclose(target.score(), np.pi / 2)


def test_2d_rotation_target():
    frameA = tf.Frame(2, name="world")
    frameB = tf.AngleJoint()(frameA)

    target = ik.RotationTarget(
        tf.AngleJoint(angle=90, degrees=True),
        frameA,
        frameB,
    )

    assert np.isclose(target.score(), np.pi / 2)
