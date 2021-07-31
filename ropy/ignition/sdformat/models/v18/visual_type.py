from dataclasses import dataclass, field
from typing import List, Optional
from .geometry_type import GeometryType
from .material_type import MaterialType
from .plugin_type import PluginType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/visual"


@dataclass
class VisualType:
    """The visual properties of the link.

    This element specifies the shape of the object (box, cylinder, etc.)
    for visualization purposes.

    Parameters
    ----------
    cast_shadows: If true the visual will cast shadows.
    laser_retro: will be implemented in the future release.
    transparency: The amount of transparency( 0=opaque, 1 = fully
        transparent)
    visibility_flags: Visibility flags of a visual. When (camera's
        visibility_mask &amp; visual's visibility_flags) evaluates to
        non-zero, the visual will be visible to the camera.
    meta: Optional meta information for the visual. The information
        contained within this element should be used to provide
        additional feedback to an end user.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
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
        }
    )
    laser_retro: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    transparency: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    visibility_flags: List[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    meta: List["VisualType.MetaType"] = field(
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
    material: List[MaterialType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    geometry: List[GeometryType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    plugin: List[PluginType] = field(
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
    class MetaType:
        """Optional meta information for the visual.

        The information contained within this element should be used to
        provide additional feedback to an end user.

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
            }
        )
