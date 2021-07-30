from dataclasses import dataclass, field
from typing import List, Optional
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/light_state"


@dataclass
class LightType:
    """
    Parameters
    ----------
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
    name: Name of the light
    """

    class Meta:
        name = "lightType"

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
