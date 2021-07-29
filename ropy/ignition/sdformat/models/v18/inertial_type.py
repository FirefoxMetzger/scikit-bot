from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/inertial"


@dataclass
class InertialType:
    """
    Parameters
    ----------
    mass: The mass of the link.
    pose: This is the pose of the inertial reference frame. The origin
        of the inertial reference frame needs to be at the center of
        gravity. The axes of the inertial reference frame do not need to
        be aligned with the principal axes of the inertia.
    inertia: The 3x3 rotational inertia matrix. Because the rotational
        inertia matrix is symmetric, only 6 above-diagonal elements of
        this matrix are specified here, using the attributes ixx, ixy,
        ixz, iyy, iyz, izz.
    """
    class Meta:
        name = "inertialType"

    mass: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    pose: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        }
    )
    inertia: List["InertialType.Inertia"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass
    class Inertia:
        ixx: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        ixy: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        ixz: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        iyy: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        iyz: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        izz: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
