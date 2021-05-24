from ropy.transform.base import Link
from xml.etree import ElementTree
from scipy.spatial.transform import Rotation
from typing import Dict, List, Tuple
import numpy as np

from ...transform import Frame
from ...transform.affine import Translation, PlanarRotation, Inverse
from ...transform._utils import rotvec_to_reflections


def create_frame_graph(urdf: str) -> Tuple[Dict[str, Frame], Dict[str, Link]]:
    """Create a frame graph from a URDF string.

    Parameters
    ----------
    urdf: TextIO
        A text buffer containing the URDF XML.

    Returns
    -------
    frames : Dict[str, Frames]
        A dict of frames (links and joints) contained in the file.
    links : Dict[str, Frames]
        A dict of links in the graph. Names are chosen based on joint names.

    Notes
    -----
    ``frames[jointName]`` will return the joint's frame that is attached to the
    parent.

    """

    tree = ElementTree.fromstring(urdf)

    frames = dict()
    links = dict()
    links_to_process: List[ElementTree.Element] = list()
    origin = dict()

    for child in tree:
        if child.tag == "link":
            frames[child.attrib["name"]] = Frame(3)
        elif child.tag == "joint":
            frames[child.attrib["name"]] = Frame(3)
            links_to_process.append(child)

    for link in links_to_process:
        frame_joint = frames[link.attrib["name"]]
        joint_type = link.attrib["type"]

        frame_offset = np.zeros(3, dtype=np.float_)
        frame_rotation = np.zeros(3, dtype=np.float_)
        for child in link:
            if child.tag == "parent":
                frame_parent = frames[child.attrib["link"]]
            elif child.tag == "child":
                frame_child = frames[child.attrib["link"]]
            elif child.tag == "origin":
                try:
                    frame_offset = child.attrib["xyz"]
                    frame_offset = -np.array(frame_offset.split(" "), dtype=np.float_)
                except KeyError:
                    frame_offset = np.zeros(3, dtype=np.float_)

                try:
                    frame_rotation = child.attrib["rpy"]
                    frame_rotation = np.array(
                        frame_rotation.split(" "), dtype=np.float_
                    )
                except KeyError:
                    frame_rotation = np.zeros(3, dtype=np.float_)
            elif child.tag == "axis":
                axis = child.attrib["xyz"]
                axis = np.array(axis.split(" "), dtype=np.float_)

        # link parent -> joint
        rotation = Rotation.from_euler("xyz", frame_rotation)
        if rotation.magnitude() > 0:
            intermediate_frame = Frame(3)
            frame_link = Translation(frame_parent, intermediate_frame, frame_offset)
            frame_parent.add_link(frame_link)
            intermediate_frame.add_link(Inverse(frame_link))

            u, v = rotvec_to_reflections(
                rotation.as_rotvec(), angle=rotation.magnitude()
            )
            frame_link = PlanarRotation(intermediate_frame, frame_joint, u, v)
            intermediate_frame.add_link(frame_link)
            frame_joint.add_link(Inverse(frame_link))
        else:
            frame_link = Translation(frame_parent, frame_joint, frame_offset)
            frame_parent.add_link(frame_link)
            frame_joint.add_link(Inverse(frame_link))

        # link joint -> child
        if joint_type == "fixed":
            frame_link = Translation(frame_joint, frame_child, (0, 0, 0))
        elif joint_type == "revolute":
            u, v = rotvec_to_reflections(axis)
            frame_link = PlanarRotation(frame_joint, frame_child, u, v)
            frame_link.angle = 0.0
        elif joint_type == "prismatic":
            frame_link = Translation(frame_joint, frame_child, -axis, amount=0)
        else:
            raise ValueError(f"Unsupported Joint type {joint_type}")

        frame_joint.add_link(frame_link)
        frame_child.add_link(Inverse(frame_link))

        links[link.attrib["name"]] = frame_link

    return frames, links
