from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/scene"


@dataclass
class SceneType:
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
        name = "sceneType"

    ambient: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        }
    )
    background: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        }
    )
    sky: List["SceneType.Sky"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    shadows: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    fog: List["SceneType.Fog"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    grid: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    origin_visual: List[bool] = field(
        default_factory=list,
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
        time: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        sunrise: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        sunset: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        clouds: List["SceneType.Sky.Clouds"] = field(
            default_factory=list,
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
            speed: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            direction: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            humidity: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            mean_size: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            ambient: List[str] = field(
                default_factory=list,
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
        color: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
            }
        )
        type: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        start: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        end: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        density: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
