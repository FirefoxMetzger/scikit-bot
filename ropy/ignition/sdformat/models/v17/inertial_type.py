from dataclasses import dataclass, field
from typing import List
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/inertial"


@dataclass
class InertialType:
    """
    Parameters
    ----------
    mass: The mass of the link.
    inertia: The 3x3 rotational inertia matrix. Because the rotational
        inertia matrix is symmetric, only 6 above-diagonal elements of
        this matrix are specified here, using the attributes ixx, ixy,
        ixz, iyy, iyz, izz.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
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
    inertia: List["InertialType.Inertia"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    pose: List[PoseType] = field(
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
