from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/box_shape"


@dataclass
class BoxType:
    """
    Box shape.

    Parameters
    ----------
    size: The three side lengths of the box. The origin of the box is in
        its geometric center (inside the center of the box).
    """
    class Meta:
        name = "boxType"

    size: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        }
    )
