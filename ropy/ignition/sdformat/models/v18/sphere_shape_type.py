from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/sphere_shape"


@dataclass
class SphereType:
    """
    Parameters
    ----------
    radius: radius of the sphere
    """
    class Meta:
        name = "sphereType"

    radius: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
