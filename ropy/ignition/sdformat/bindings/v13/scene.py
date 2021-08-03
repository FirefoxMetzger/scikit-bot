from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/v1.3/scene.xsd"


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
    """
    class Meta:
        name = "scene"

    ambient: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        }
    )
    background: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        }
    )
    sky: Optional["Scene.Sky"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    shadows: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    fog: Optional["Scene.Fog"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    grid: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
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
        time: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        sunrise: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        sunset: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        clouds: Optional["Scene.Sky.Clouds"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
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
            speed: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            direction: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            humidity: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            mean_size: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            ambient: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
                }
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
        color: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
            }
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        start: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        end: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        density: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
