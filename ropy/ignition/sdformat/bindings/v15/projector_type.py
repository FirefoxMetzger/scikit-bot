from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .plugin_type import PluginType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/projector"


@dataclass
class ProjectorType:
    """
    Parameters
    ----------
    texture: Texture name
    fov: Field of view
    near_clip: Near clip distance
    far_clip: far clip distance
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    name: Name of the projector
    """

    class Meta:
        name = "projectorType"

    texture: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    fov: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    near_clip: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    far_clip: List[float] = field(
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
    plugin: List[PluginType] = field(
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
