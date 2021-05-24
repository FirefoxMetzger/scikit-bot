import pytest

import ropy.ros as pyros


@pytest.fixture()
def compi_robot():
    COMPI_URDF = """<?xml version="1.0"?>
    <robot name="compi">
    <link name="linkmount"/>
    <link name="link1"/>
    <link name="link2"/>
    <link name="link3"/>
    <link name="link4"/>
    <link name="link5"/>
    <link name="link6"/>
    <link name="tcp"/>
    <joint name="joint1" type="revolute">
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <parent link="linkmount"/>
    <child link="link1"/>
    <axis xyz="0 0 1.0"/>
    <limit lower="-1" upper="1"/>
    </joint>
    <joint name="joint2" type="revolute">
    <origin xyz="0 0 0.158" rpy="1.570796 0 0"/>
    <parent link="link1"/>
    <child link="link2"/>
    <axis xyz="0 0 -1.0"/>
    <limit lower="-1"/>
    </joint>
    <joint name="joint3" type="revolute">
    <origin xyz="0 0.28 0" rpy="0 0 0"/>
    <parent link="link2"/>
    <child link="link3"/>
    <axis xyz="0 0 -1.0"/>
    <limit upper="1"/>
    </joint>
    <joint name="joint4" type="revolute">
    <origin xyz="0 0 0" rpy="-1.570796 0 0"/>
    <parent link="link3"/>
    <child link="link4"/>
    <axis xyz="0 0 1.0"/>
    </joint>
    <joint name="joint5" type="revolute">
    <origin xyz="0 0 0.34" rpy="1.570796 0 0"/>
    <parent link="link4"/>
    <child link="link5"/>
    <axis xyz="0 0 -1.0"/>
    </joint>
    <joint name="joint6" type="revolute">
    <origin xyz="0 0.346 0" rpy="-1.570796 0 0"/>
    <parent link="link5"/>
    <child link="link6"/>
    <axis xyz="0 0 1.0"/>
    </joint>
    <joint name="jointtcp" type="fixed">
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <parent link="link6"/>
    <child link="tcp"/>
    </joint>
    <transmission name="joint1_trans">
    <type>transmission_interface/SimpleTransmission</type>
    <joint name="joint1">
        <hardwareInterface>PositionJointInterface</hardwareInterface>
    </joint>
    <actuator name="joint1_motor">
        <mechanicalReduction>1</mechanicalReduction>
    </actuator>
    </transmission>
    </robot>"""
    frames, links = pyros.create_frame_graph(COMPI_URDF)
    return frames, links


@pytest.fixture()
def two_parents():
    urdf = """<?xml version="1.0"?>
        <robot name="mmm">
            <link name="parent0"/>
            <link name="parent1"/>
            <link name="child"/>
            <joint name="joint0" type="revolute">
                <origin xyz="1 0 0" rpy="0 0 0"/>
                <parent link="parent0"/>
                <child link="child"/>
                <axis xyz="1 0 0"/>
            </joint>
            <joint name="joint1" type="revolute">
                <origin xyz="0 1 0" rpy="0 0 0"/>
                <parent link="parent1"/>
                <child link="child"/>
                <axis xyz="1 0 0"/>
            </joint>
        </robot>
        """
    frames, links = pyros.create_frame_graph(urdf)
    return (frames, links)


@pytest.fixture()
def simple_prismatic():
    urdf = """<?xml version="1.0"?>
        <robot name="mmm">
            <link name="parent"/>
            <link name="child"/>
            <joint name="joint" type="prismatic">
                <origin xyz="0 0 0" rpy="0 0 0"/>
                <parent link="parent"/>
                <child link="child"/>
                <axis xyz="1 0 0"/>
            </joint>
        </robot>
        """
    frames, links = pyros.create_frame_graph(urdf)
    return (frames, links)
