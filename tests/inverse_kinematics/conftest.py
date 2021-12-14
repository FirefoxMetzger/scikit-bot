import pytest
import skbot.ignition as ign
import skbot.transform as tf
from typing import Tuple, List, Union
from pathlib import Path


joint_types = Union[tf.RotationalJoint, tf.PrismaticJoint]
sdf_folder = Path(__file__).parents[1] / "ignition" / "sdf"


@pytest.fixture()
def panda():
    sdf_string = (sdf_folder / "robots" / "panda" / "model.sdf").read_text()
    base_frame = ign.sdformat.to_frame_graph(sdf_string)

    tool_frame = base_frame.find_frame(".../panda_link8")

    joints = list()
    for link in tool_frame.links_between(base_frame):
        if isinstance(link, (tf.RotationalJoint, tf.PrismaticJoint)):
            joints.append(link)

    for value, joint in zip([0, -0.785, 0, -2.356, 0, 1.571, 0.785], reversed(joints)):
        joint.param = value
    return base_frame, joints


@pytest.fixture()
def double_pendulum():
    sdf_string = (sdf_folder / "robots" / "double_pendulum" / "model.sdf").read_text()
    base_frame = ign.sdformat.to_frame_graph(sdf_string)

    tool_frame = base_frame.find_frame(".../lower_link")

    joints = list()
    for link in tool_frame.links_between(base_frame):
        if isinstance(link, (tf.RotationalJoint, tf.PrismaticJoint)):
            joints.append(link)

    return base_frame, joints


@pytest.fixture()
def circle_bot():
    world = tf.Frame(3, name="world")
    ellbow = tf.Frame(3, name="ellbow")
    tool = tf.Frame(3, name="tool")

    rotate = tf.RotationalJoint((0, 0, 1), angle=0)
    reach = tf.PrismaticJoint((-1, 0, 0), upper_limit=10, lower_limit=-10)

    rotate(world, ellbow)
    reach(ellbow, tool)

    return world, [rotate, reach]
