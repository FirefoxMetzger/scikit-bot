from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/link_state"


@dataclass
class LinkType:
    """
    Link state.

    Parameters
    ----------
    velocity: Velocity of the link. The x, y, z components of the pose
        correspond to the linear velocity of the link, and the roll,
        pitch, yaw components correspond to the angular velocity of the
        link
    acceleration: Acceleration of the link. The x, y, z components of
        the pose correspond to the linear acceleration of the link, and
        the roll, pitch, yaw components correspond to the angular
        acceleration of the link
    wrench: Force and torque applied to the link. The x, y, z components
        of the pose correspond to the force applied to the link, and the
        roll, pitch, yaw components correspond to the torque applied to
        the link
    collision: Collision state
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    name: Name of the link
    """

    class Meta:
        name = "linkType"

    velocity: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    acceleration: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    wrench: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    collision: List["LinkType.Collision"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    frame: List[FrameType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: List[PoseType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Collision:
        """
        Collision state.

        Parameters
        ----------
        name: Name of the collision
        """

        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
