from dataclasses import dataclass, field
from typing import List, Optional
from .material_type import MaterialType

__NAMESPACE__ = "sdformat/road"


@dataclass
class RoadType:
    """
    Parameters
    ----------
    width: Width of the road
    point: A series of points that define the path of the road.
    material: The material of the visual element.
    name: Name of the road
    """
    class Meta:
        name = "roadType"

    width: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    point: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        }
    )
    material: List[MaterialType] = field(
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
