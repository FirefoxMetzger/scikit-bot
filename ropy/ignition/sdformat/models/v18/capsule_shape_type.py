from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/capsule_shape"


@dataclass
class CapsuleType:
    """
    Capsule shape.

    Parameters
    ----------
    radius: Radius of the capsule
    length: Length of the cylindrical portion of the capsule along the z
        axis
    """

    class Meta:
        name = "capsuleType"

    radius: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    length: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
