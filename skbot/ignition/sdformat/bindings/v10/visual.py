from dataclasses import dataclass, field
from typing import Optional
from .geometry import Geometry

__NAMESPACE__ = "sdformat/v1.0/visual.xsd"


@dataclass
class Visual:
    class Meta:
        name = "visual"

    origin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
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
    cast_shadows: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )
    laser_retro: float = field(
        default=0.0,
        metadata={
            "type": "Attribute",
        },
    )
    transparency: float = field(
        default=0.0,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class Material:
        shader: Optional["Visual.Material.Shader"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        ambient: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        diffuse: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        specular: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        emissive: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        script: str = field(
            default="__default__",
            metadata={
                "type": "Attribute",
            },
        )

        @dataclass
        class Shader:
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
