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
        respect to the frame named in the relative_to attribute.
    name: Name of the frame. This name must not match another frame
        defined inside the parent that this frame is attached to.
    attached_to: Name of the link or frame to which this frame is
        attached. If a frame is specified, recursively following the
        attached_to attributes of the specified frames must lead to the
        name of a link, a model, or the world frame.
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
    attached_to: str = field(
        default="",
        metadata={
            "type": "Attribute",
        }
    )
