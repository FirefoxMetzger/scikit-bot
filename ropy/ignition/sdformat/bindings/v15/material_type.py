from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/material"


@dataclass
class MaterialType:
    """
    The material of the visual element.

    Parameters
    ----------
    script: Name of material from an installed script file. This will
        override the color element if the script exists.
    shader:
    lighting: If false, dynamic lighting will be disabled
    ambient: The ambient color of a material specified by set of four
        numbers representing red/green/blue, each in the range of [0,1].
    diffuse: The diffuse color of a material specified by set of four
        numbers representing red/green/blue/alpha, each in the range of
        [0,1].
    specular: The specular color of a material specified by set of four
        numbers representing red/green/blue/alpha, each in the range of
        [0,1].
    emissive: The emissive color of a material specified by set of four
        numbers representing red/green/blue, each in the range of [0,1].
    """

    class Meta:
        name = "materialType"

    script: List["MaterialType.Script"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    shader: List["MaterialType.Shader"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    lighting: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    ambient: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    diffuse: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    specular: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    emissive: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
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

        uri: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        name: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
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

        normal_map: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
