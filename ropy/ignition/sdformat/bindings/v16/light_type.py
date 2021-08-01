from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/light"


@dataclass
class LightType:
    """
    The light element describes a light source.

    Parameters
    ----------
    cast_shadows: When true, the light will cast shadows.
    diffuse: Diffuse light color
    specular: Specular light color
    attenuation: Light attenuation
    direction: Direction of the light, only applicable for spot and
        directional lights.
    spot: Spot light parameters
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    name: A unique name for the light.
    type: The light type: point, directional, spot.
    """

    class Meta:
        name = "lightType"

    cast_shadows: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
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
    attenuation: List["LightType.Attenuation"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    direction: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    spot: List["LightType.Spot"] = field(
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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

    @dataclass
    class Attenuation:
        """
        Light attenuation.

        Parameters
        ----------
        range: Range of the light
        linear: The linear attenuation factor: 1 means attenuate evenly
            over the distance.
        constant: The constant attenuation factor: 1.0 means never
            attenuate, 0.0 is complete attenutation.
        quadratic: The quadratic attenuation factor: adds a curvature to
            the attenuation.
        """

        range: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        linear: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        constant: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        quadratic: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Spot:
        """
        Spot light parameters.

        Parameters
        ----------
        inner_angle: Angle covered by the bright inner cone
        outer_angle: Angle covered by the outer cone
        falloff: The rate of falloff between the inner and outer cones.
            1.0 means a linear falloff, less means slower falloff,
            higher means faster falloff.
        """

        inner_angle: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        outer_angle: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        falloff: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
