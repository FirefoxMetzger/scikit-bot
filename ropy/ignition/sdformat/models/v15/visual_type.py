from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .geometry_type import GeometryType
from .material_type import MaterialType
from .plugin_type import PluginType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/visual"


@dataclass
class VisualType:
    """
    Parameters
    ----------
    cast_shadows: If true the visual will cast shadows.
    laser_retro: will be implemented in the future release.
    transparency: The amount of transparency( 0=opaque, 1 = fully
        transparent)
    meta: Optional meta information for the visual. The information
        contained within this element should be used to provide
        additional feedback to an end user.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    material: The material of the visual element.
    geometry: The shape of the visual or collision object.
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    name: Unique name for the visual element within the scope of the
        parent link.
    """

    class Meta:
        name = "visualType"

    cast_shadows: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    laser_retro: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    transparency: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    meta: List["VisualType.MetaType"] = field(
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
    material: List[MaterialType] = field(
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

    @dataclass
    class MetaType:
        """
        Parameters
        ----------
        layer: The layer in which this visual is displayed. The layer
            number is useful for programs, such as Gazebo, that put
            visuals in different layers for enhanced visualization.
        """

        layer: List[int] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
