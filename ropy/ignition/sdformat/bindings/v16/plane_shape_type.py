from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/plane_shape"


@dataclass
class PlaneType:
    """
    Plane shape.

    Parameters
    ----------
    normal: Normal direction for the plane. When a Plane is used as a
        geometry for a Visual or Collision object, then the normal is
        specified in the Visual or Collision frame, respectively.
    size: Length of each side of the plane. Note that this property is
        meaningful only for visualizing the Plane, i.e., when the Plane
        is used as a geometry for a Visual object. The Plane has
        infinite size when used as a geometry for a Collision object.
    """
    class Meta:
        name = "planeType"

    normal: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        }
    )
    size: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+)((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        }
    )
