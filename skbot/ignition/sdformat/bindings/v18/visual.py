from dataclasses import dataclass, field
from typing import List, Optional
from .geometry import Geometry
from .material import Material

__NAMESPACE__ = "sdformat/v1.8/visual.xsd"


@dataclass
class Visual:
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
        name = "visual"

    cast_shadows: bool = field(
        default=True,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    laser_retro: float = field(
        default=0.0,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    transparency: float = field(
        default=0.0,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    visibility_flags: int = field(
        default=4294967295,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    meta: Optional["Visual.MetaType"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: "Visual.Pose" = field(
        default="0 0 0 0 0 0",
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    material: Optional[Material] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    geometry: Optional[Geometry] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    plugin: List["Visual.Plugin"] = field(
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
        """Optional meta information for the visual.

        The information contained within this element should be used to
        provide additional feedback to an end user.

        Parameters
        ----------
        layer: The layer in which this visual is displayed. The layer
            number is useful for programs, such as Gazebo, that put
            visuals in different layers for enhanced visualization.
        """

        layer: int = field(
            default=0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Pose:
        """
        Parameters
        ----------
        value:
        relative_to: Name of frame relative to which the pose is
            applied.
        """

        value: Optional[str] = field(
            default=None,
            metadata={
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        relative_to: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class Plugin:
        """A plugin is a dynamically loaded chunk of code.

        It can exist as a child of world, model, and sensor.

        Parameters
        ----------
        any_element: This is a special element that should not be
            specified in an SDFormat file. It automatically copies child
            elements into the SDFormat element so that a plugin can
            access the data.
        name: A unique name for the plugin, scoped to its parent.
        filename: Name of the shared library to load. If the filename is
            not a full path name, the file will be searched for in the
            configuration paths.
        """

        any_element: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        filename: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
