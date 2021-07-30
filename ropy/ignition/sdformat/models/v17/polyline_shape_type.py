from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/polyline_shape"


@dataclass
class PolylineType:
    """
    Parameters
    ----------
    point: A series of points that define the path of the polyline.
    height: Height of the polyline
    """

    class Meta:
        name = "polylineType"

    point: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+)((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    height: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
