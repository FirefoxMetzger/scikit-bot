from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/v1.5/light.xsd"


@dataclass
class Light:
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
        name = "light"

    cast_shadows: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    diffuse: str = field(
        default="1 1 1 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    specular: str = field(
        default=".1 .1 .1 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    attenuation: Optional["Light.Attenuation"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    direction: str = field(
        default="0 0 -1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    spot: Optional["Light.Spot"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    frame: List["Light.Frame"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: "Light.Pose" = field(
        default="0 0 0 0 0 0",
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: str = field(
        default="__default__",
        metadata={
            "type": "Attribute",
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

        range: float = field(
            default=10.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        linear: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        constant: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        quadratic: float = field(
            default=0.0,
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

        inner_angle: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        outer_angle: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        falloff: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Frame:
        """
        A frame of reference to which a pose is relative.

        Parameters
        ----------
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the specified frame.
        name: Name of the frame. This name must not match another frame
            defined inside the parent that this frame is attached to.
        """

        pose: "Light.Frame.Pose" = field(
            default="0 0 0 0 0 0",
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
        class Pose:
            """
            Parameters
            ----------
            value:
            frame: Name of frame which the pose is defined relative to.
            """

            value: Optional[str] = field(
                default=None,
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            frame: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass
    class Pose:
        """
        Parameters
        ----------
        value:
        frame: Name of frame which the pose is defined relative to.
        """

        value: Optional[str] = field(
            default=None,
            metadata={
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        frame: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )
