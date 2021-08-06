from typing import Dict
import numpy as np
import skbot.transform as rtf
import skbot.ros as pyros
import pytest


def test_frame_graph(compi_robot):
    frames: Dict[str, rtf.Frame]
    frames, links = compi_robot
    tf = frames["link6"].get_affine_matrix(frames["linkmount"])
    expected = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1.124], [0, 0, 0, 1]])

    np.allclose(tf, expected)


def test_without_origin():
    urdf = """<?xml version="1.0"?>
        <robot name="robot_name">
        <link name="link0"/>
        <link name="link1"/>
        <joint name="joint0" type="fixed">
            <parent link="link0"/>
            <child link="link1"/>
        </joint>
        </robot>
        """
    frames, _ = pyros.create_frame_graph(urdf)
    link1_to_link0 = frames["link0"].get_affine_matrix(frames["link1"])
    np.allclose(link1_to_link0, np.eye(4))


def test_with_empty_origin():
    urdf = """<?xml version="1.0"?>
    <robot name="robot_name">
    <link name="link0"/>
    <link name="link1"/>
    <joint name="joint0" type="fixed">
        <parent link="link0"/>
        <child link="link1"/>
        <origin/>
    </joint>
    </robot>
    """
    frames, _ = pyros.create_frame_graph(urdf)
    link1_to_link0 = frames["link0"].get_affine_matrix(frames["link1"])
    np.allclose(link1_to_link0, np.eye(4))


def test_joint_angles(compi_robot):
    frames: Dict[str, rtf.Frame]
    links: Dict[str, rtf.Link]
    frames, links = compi_robot

    for i in range(1, 7):
        links[f"joint{i}"].angle = 0.1 * i

    tf = frames["link6"].get_affine_matrix(frames["linkmount"])
    np.allclose(
        tf,
        np.array(
            [
                [0.121698, -0.606672, 0.785582, 0.489351],
                [0.818364, 0.509198, 0.266455, 0.114021],
                [-0.561668, 0.610465, 0.558446, 0.924019],
                [0.0, 0.0, 0.0, 1.0],
            ]
        ),
    )


def test_fixed_joint(compi_robot):
    frames: Dict[str, rtf.Frame]
    frames, _ = compi_robot

    tf = frames["tcp"].get_affine_matrix(frames["linkmount"])
    np.allclose(
        tf, np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1.174], [0, 0, 0, 1]])
    )


def test_multiple_parents(two_parents):
    frames: Dict[str, rtf.Frame]
    frames, _ = two_parents

    tf1 = frames["parent0"].get_affine_matrix(frames["child"])
    tf2 = frames["parent1"].get_affine_matrix(frames["child"])
    np.allclose(tf1[0, 3], tf2[1, 3])


def test_prismatic_joint(simple_prismatic):
    frames: Dict[str, rtf.Frame]
    links: Dict[str, rtf.Link]
    frames, links = simple_prismatic

    links["joint"].amount = 5.33
    tf = frames["parent"].get_affine_matrix(frames["child"])

    np.allclose(
        tf, np.array([[1, 0, 0, 5.33], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    )


def test_unkown_joint():
    urdf = """<?xml version="1.0"?>
            <robot name="mmm">
                <link name="parent"/>
                <link name="child"/>
                <joint name="joint" type="unknown">
                    <origin xyz="0 0 0" rpy="0 0 0"/>
                    <parent link="parent"/>
                    <child link="child"/>
                    <axis xyz="1 0 0"/>
                </joint>
            </robot>
            """

    with pytest.raises(ValueError):
        frames, links = pyros.create_frame_graph(urdf)
