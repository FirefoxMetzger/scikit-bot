from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/pose"


@dataclass
class PoseType:
    """
    A position(x,y,z) and orientation(roll, pitch yaw) with respect to the
    specified frame.

    Parameters
    ----------
    value:
    frame: Name of frame which the pose is defined relative to.
    """
    class Meta:
        name = "poseType"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        }
    )
    frame: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
