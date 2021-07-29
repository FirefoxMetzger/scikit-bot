from dataclasses import dataclass, field
from typing import List, Optional
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/frame"


@dataclass
class FrameType:
    """
    Parameters
    ----------
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    name: Name of the frame. This name must not match another frame
        defined inside the parent that this frame is attached to.
    """
    class Meta:
        name = "frameType"

    pose: List[PoseType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
