from skbot.transform import base
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
