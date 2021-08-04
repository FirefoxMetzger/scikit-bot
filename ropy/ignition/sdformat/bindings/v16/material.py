from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/v1.6/material.xsd"


@dataclass
class Material:
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
    pbr: Physically Based Rendering (PBR) material. There are two PBR
        workflows: metal and specular. While both workflows and their
        parameters can be specified at the same time, typically only one
        of them will be used (depending on the underlying renderer
        capability). It is also recommended to use the same workflow for
        all materials in the world.
    """

    class Meta:
        name = "material"

    script: Optional["Material.Script"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    shader: Optional["Material.Shader"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    lighting: bool = field(
        default=True,
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
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    diffuse: str = field(
        default="0 0 0 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    specular: str = field(
        default="0 0 0 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    emissive: str = field(
        default="0 0 0 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    pbr: Optional["Material.Pbr"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
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
                "min_occurs": 1,
            },
        )
        name: str = field(
            default="__default__",
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

        normal_map: str = field(
            default="__default__",
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

    @dataclass
    class Pbr:
        """Physically Based Rendering (PBR) material.

        There are two PBR workflows: metal and specular. While both
        workflows and their parameters can be specified at the same
        time, typically only one of them will be used (depending on the
        underlying renderer capability). It is also recommended to use
        the same workflow for all materials in the world.

        Parameters
        ----------
        metal: PBR using the Metallic/Roughness workflow.
        specular: PBR using the Specular/Glossiness workflow.
        """

        metal: Optional["Material.Pbr.Metal"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        specular: Optional["Material.Pbr.Specular"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Metal:
            """
            PBR using the Metallic/Roughness workflow.

            Parameters
            ----------
            albedo_map: Filename of the diffuse/albedo map.
            roughness_map: Filename of the roughness map.
            roughness: Material roughness in the range of [0,1], where 0
                represents a smooth surface and 1 represents a rough
                surface. This is the inverse of a specular map in a PBR
                specular workflow.
            metalness_map: Filename of the metalness map.
            metalness: Material metalness in the range of [0,1], where 0
                represents non-metal and 1 represents raw metal
            environment_map: Filename of the environment / reflection
                map, typically in the form of a cubemap
            ambient_occlusion_map: Filename of the ambient occlusion
                map. The map defines the amount of ambient lighting on
                the surface.
            normal_map: Filename of the normal map. The normals can be
                in the object space or tangent space as specified in the
                'type' attribute
            emissive_map: Filename of the emissive map.
            """

            albedo_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            roughness_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            roughness: str = field(
                default="0.5",
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            metalness_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            metalness: str = field(
                default="0.5",
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            environment_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            ambient_occlusion_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            normal_map: Optional["Material.Pbr.Metal.NormalMap"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            emissive_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class NormalMap:
                """
                Parameters
                ----------
                value:
                type: The space that the normals are in. Values are:
                    'object' or 'tangent'
                """

                value: Optional[str] = field(
                    default=None,
                    metadata={
                        "required": True,
                    },
                )
                type: str = field(
                    default="tangent",
                    metadata={
                        "type": "Attribute",
                    },
                )

        @dataclass
        class Specular:
            """
            PBR using the Specular/Glossiness workflow.

            Parameters
            ----------
            albedo_map: Filename of the diffuse/albedo map.
            specular_map: Filename of the specular map.
            glossiness_map: Filename of the glossiness map.
            glossiness: Material glossiness in the range of [0-1], where
                0 represents a rough surface and 1 represents a smooth
                surface. This is the inverse of a roughness map in a PBR
                metal workflow.
            ambient_occlusion_map: Filename of the ambient occlusion
                map. The map defines the amount of ambient lighting on
                the surface.
            normal_map: Filename of the normal map. The normals can be
                in the object space or tangent space as specified in the
                'type' attribute
            emissive_map: Filename of the emissive map.
            """

            albedo_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            specular_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            glossiness_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            glossiness: str = field(
                default="0",
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            ambient_occlusion_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            normal_map: Optional["Material.Pbr.Specular.NormalMap"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            emissive_map: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class NormalMap:
                """
                Parameters
                ----------
                value:
                type: The space that the normals are in. Values are:
                    'object' or 'tangent'
                """

                value: Optional[str] = field(
                    default=None,
                    metadata={
                        "required": True,
                    },
                )
                type: str = field(
                    default="tangent",
                    metadata={
                        "type": "Attribute",
                    },
                )
