from dataclasses import dataclass, field
from typing import List, Optional
from .audio_sink_type import AudioSinkType
from .audio_source_type import AudioSourceType
from .battery_type import BatteryType
from .collision_type import CollisionType
from .frame_type import FrameType
from .inertial_type import InertialType
from .pose_type import PoseType
from .projector_type import ProjectorType
from .sensor_type import SensorType
from .visual_type import VisualType

__NAMESPACE__ = "sdformat/link"


@dataclass
class LinkType:
    """
    Parameters
    ----------
    gravity: If true, the link is affected by gravity.
    self_collide: If true, the link can collide with other links in the
        model. Two links within a model will collide if
        link1.self_collide OR link2.self_collide. Links connected by a
        joint will never collide.
    kinematic: If true, the link is kinematic only
    must_be_base_link: If true, the link will have 6DOF and be a direct
        child of world.
    velocity_decay: Exponential damping of the link's velocity.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    inertial: The inertial properties of the link.
    collision: The collision properties of a link. Note that this can be
        different from the visual properties of a link, for example,
        simpler collision models are often used to reduce computation
        time.
    visual: The visual properties of the link. This element specifies
        the shape of the object (box, cylinder, etc.) for visualization
        purposes.
    sensor: The sensor tag describes the type and properties of a
        sensor.
    projector:
    audio_sink: An audio sink.
    audio_source: An audio source.
    battery: Description of a battery.
    name: A unique name for the link within the scope of the model.
    """
    class Meta:
        name = "linkType"

    gravity: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    self_collide: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    kinematic: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    must_be_base_link: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    velocity_decay: List["LinkType.VelocityDecay"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    frame: List[FrameType] = field(
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
    inertial: List[InertialType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    collision: List[CollisionType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    visual: List[VisualType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    sensor: List[SensorType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    projector: List[ProjectorType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    audio_sink: List[AudioSinkType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    audio_source: List[AudioSourceType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    battery: List[BatteryType] = field(
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

    @dataclass
    class VelocityDecay:
        """
        Parameters
        ----------
        linear: Linear damping
        angular: Angular damping
        """
        linear: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        angular: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
