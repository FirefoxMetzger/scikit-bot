from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/pose"


@dataclass
class PoseType:
    """
    Parameters
    ----------
    value:
    relative_to: Name of frame relative to which the pose is applied.
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
    relative_to: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
