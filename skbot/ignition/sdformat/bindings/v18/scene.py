from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/v1.8/scene.xsd"


@dataclass
class Scene:
    """
    Specifies the look of the environment.

    Parameters
    ----------
    ambient: Color of the ambient light.
    background: Color of the background.
    sky: Properties for the sky
    shadows: Enable/disable shadows
    fog: Controls fog
    grid: Enable/disable the grid
    origin_visual: Show/hide world origin indicator
    """

    class Meta:
        name = "scene"

    ambient: str = field(
        default="0.4 0.4 0.4 1.0",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    background: str = field(
        default=".7 .7 .7 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    sky: Optional["Scene.Sky"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    shadows: bool = field(
        default=True,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    fog: Optional["Scene.Fog"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    grid: bool = field(
        default=True,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    origin_visual: bool = field(
        default=True,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass
    class Sky:
        """
        Properties for the sky.

        Parameters
        ----------
        time: Time of day [0..24]
        sunrise: Sunrise time [0..24]
        sunset: Sunset time [0..24]
        clouds: Sunset time [0..24]
        """

        time: float = field(
            default=10.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        sunrise: float = field(
            default=6.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        sunset: float = field(
            default=20.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        clouds: Optional["Scene.Sky.Clouds"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Clouds:
            """
            Sunset time [0..24]

            Parameters
            ----------
            speed: Speed of the clouds
            direction: Direction of the cloud movement
            humidity: Density of clouds
            mean_size: Average size of the clouds
            ambient: Ambient cloud color
            """

            speed: float = field(
                default=0.6,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            direction: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            humidity: float = field(
                default=0.5,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            mean_size: float = field(
                default=0.5,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            ambient: str = field(
                default=".8 .8 .8 1",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
                },
            )

    @dataclass
    class Fog:
        """
        Controls fog.

        Parameters
        ----------
        color: Fog color
        type: Fog type: constant, linear, quadratic
        start: Distance to start of fog
        end: Distance to end of fog
        density: Density of fog
        """

        color: str = field(
            default="1 1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
            },
        )
        type: str = field(
            default="none",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        start: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        end: float = field(
            default=100.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        density: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
