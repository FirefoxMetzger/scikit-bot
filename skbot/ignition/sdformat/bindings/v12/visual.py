from dataclasses import dataclass, field
from typing import Optional
from .geometry import Geometry

__NAMESPACE__ = "sdformat/v1.2/visual.xsd"


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
    pose: Origin of the visual relative to its parent.
    material: The material of the visual element.
    geometry: The shape of the visual or collision object.
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
            "required": True,
        },
    )
    laser_retro: float = field(
        default=0.0,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    transparency: float = field(
        default=0.0,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    pose: str = field(
        default="0 0 0 0 0 0",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    material: Optional["Visual.Material"] = field(
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Material:
        """
        The material of the visual element.

        Parameters
        ----------
        script: Name of material from an installed script file. This
            will override the color element if the script exists.
        shader:
        ambient: The ambient color of a material specified by set of
            four numbers representing red/green/blue, each in the range
            of [0,1].
        diffuse: The diffuse color of a material specified by set of
            four numbers representing red/green/blue/alpha, each in the
            range of [0,1].
        specular: The specular color of a material specified by set of
            four numbers representing red/green/blue/alpha, each in the
            range of [0,1].
        emissive: The emissive color of a material specified by set of
            four numbers representing red/green/blue, each in the range
            of [0,1].
        """

        script: Optional["Visual.Material.Script"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        shader: Optional["Visual.Material.Shader"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        ambient: str = field(
            default="0 0 0 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
            },
        )
        diffuse: str = field(
            default="0 0 0 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
            },
        )
        specular: str = field(
            default="0 0 0 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
            },
        )
        emissive: str = field(
            default="0 0 0 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
            },
        )

        @dataclass
        class Script:
            """Name of material from an installed script file.

            This will override the color element if the script exists.

            Parameters
            ----------
            uri: URI of the material script file
            name: Name of the script within the script file
            """

            uri: str = field(
                default="__default__",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            name: str = field(
                default="__default__",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Shader:
            """
            Parameters
            ----------
            normal_map: filename of the normal map
            type: vertex, pixel, normal_map_object_space,
                normal_map_tangent_space
            """

            normal_map: str = field(
                default="__default__",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            type: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
