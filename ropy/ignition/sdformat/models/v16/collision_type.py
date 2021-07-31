from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .geometry_type import GeometryType
from .pose_type import PoseType
from .surface_type import SurfaceType

__NAMESPACE__ = "sdformat/collision"


@dataclass
class CollisionType:
    """The collision properties of a link.

    Note that this can be different from the visual properties of a
    link, for example, simpler collision models are often used to reduce
    computation time.

    Parameters
    ----------
    laser_retro: intensity value returned by laser sensor.
    max_contacts: Maximum number of contacts allowed between two
        entities. This value overrides the max_contacts element defined
        in physics.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    geometry: The shape of the visual or collision object.
    surface: The surface parameters
    name: Unique name for the collision element within the scope of the
        parent link.
    """

    class Meta:
        name = "collisionType"

    laser_retro: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    max_contacts: List[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    frame: List[FrameType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: List[PoseType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    geometry: List[GeometryType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    surface: List[SurfaceType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
