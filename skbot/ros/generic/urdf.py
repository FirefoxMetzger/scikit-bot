from xml.etree import ElementTree
from scipy.spatial.transform import Rotation
from typing import Dict, List, Tuple
import numpy as np

from ... import transform as rtf


def create_frame_graph(urdf: str) -> Tuple[Dict[str, rtf.Frame], Dict[str, rtf.Link]]:
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

    See Also
    --------
    :mod:`skbot.transform`

    Notes
    -----
    ``frames[jointName]`` will return the joint's frame that is attached to the
    parent.

    """

    tree = ElementTree.fromstring(urdf)

    frames = dict()
    links = dict()
    links_to_process: List[ElementTree.Element] = list()

    for child in tree:
        if child.tag == "link":
            frames[child.attrib["name"]] = rtf.Frame(3, name=child.attrib["name"])
        elif child.tag == "joint":
            frames[child.attrib["name"]] = rtf.Frame(3, name=child.attrib["name"])
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
            intermediate_frame = rtf.EulerRotation("xyz", frame_rotation)(frame_parent)
            rtf.affine.Translation(frame_offset)(intermediate_frame, frame_joint)
        else:
            rtf.affine.Translation(frame_offset)(frame_parent, frame_joint)

        # link joint -> child
        if joint_type == "fixed":
            frame_link = rtf.affine.Translation((0, 0, 0))
        elif joint_type == "revolute":
            frame_link = rtf.RotvecRotation(axis, angle=0)
        elif joint_type == "prismatic":
            frame_link = rtf.affine.Translation(-axis, amount=0)
        else:
            raise ValueError(f"Unsupported Joint type {joint_type}")

        frame_link(frame_joint, frame_child)

        links[link.attrib["name"]] = frame_link

    return frames, links
