from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/light_state"


@dataclass
class LightType:
    """
    Light state.

    Parameters
    ----------
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    name: Name of the light
    """

    class Meta:
        name = "lightType"

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
