from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/cylinder_shape"


@dataclass
class CylinderType:
    """
    Cylinder shape.

    Parameters
    ----------
    radius: Radius of the cylinder
    length: Length of the cylinder along the z axis
    """
    class Meta:
        name = "cylinderType"

    radius: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    length: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
