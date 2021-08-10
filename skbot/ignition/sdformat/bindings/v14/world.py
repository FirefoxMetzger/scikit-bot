from dataclasses import dataclass, field
from typing import List, Optional
from .actor import Actor
from .joint import Joint
from .light import Light
from .model import Model
from .physics import Physics
from .scene import Scene
from .state import State

__NAMESPACE__ = "sdformat/v1.4/world.xsd"


@dataclass
class World:
    """
    The world element encapsulates an entire world description including:
    models, scene, physics, joints, and plugins.

    Parameters
    ----------
    audio: Global audio properties.
    include: Include resources from a URI
    gui:
    physics: The physics tag specifies the type and properties of the
        dynamics engine.
    scene: Specifies the look of the environment.
    light: The light element describes a light source.
    model: The model element defines a complete robot or any other
        physical object.
    actor:
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    joint: A joint connections two links with kinematic and dynamic
        properties.
    road:
    spherical_coordinates:
    state:
    name: Unique name of the world
    """

    class Meta:
        name = "world"

    audio: Optional["World.Audio"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    include: List["World.Include"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gui: Optional["World.Gui"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    physics: Optional[Physics] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    scene: Optional[Scene] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    light: List[Light] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    model: List[Model] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    actor: List[Actor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    plugin: List["World.Plugin"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    joint: List[Joint] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    road: List["World.Road"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    spherical_coordinates: Optional["World.SphericalCoordinates"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    state: List[State] = field(
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
    class Audio:
        """
        Global audio properties.

        Parameters
        ----------
        device: Device to use for audio playback. A value of "default"
            will use the system's default audio device. Otherwise,
            specify a an audio device file"
        """

        device: str = field(
            default="default",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

    @dataclass
    class Include:
        """
        Include resources from a URI.

        Parameters
        ----------
        uri: URI to a resource, such as a model
        """

        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

    @dataclass
    class Gui:
        camera: Optional["World.Gui.Camera"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        fullscreen: bool = field(
            default=False,
            metadata={
                "type": "Attribute",
            },
        )

        @dataclass
        class Camera:
            view_controller: str = field(
                default="orbit",
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
            track_visual: Optional["World.Gui.Camera.TrackVisual"] = field(
                default=None,
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
            class TrackVisual:
                name: str = field(
                    default="__default__",
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                min_dist: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                    },
                )
                max_dist: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
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

    @dataclass
    class Road:
        """
        Parameters
        ----------
        width: Width of the road
        point: A series of points define the path of the road.
        name: Name of the road
        """

        width: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        point: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
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
    class SphericalCoordinates:
        """
        Parameters
        ----------
        surface_model: Name of planetary surface model, used to
            determine the surface altitude       at a given latitude and
            longitude. The default is an ellipsoid model of       the
            earth based on the WGS-84 standard. It is used in Gazebo's
            GPS sensor       implementation.
        latitude_deg: Geodetic latitude at origin of gazebo reference
            frame, specified       in units of degrees.
        longitude_deg: Longitude at origin of gazebo reference frame,
            specified in units       of degrees.
        elevation: Elevation of origin of gazebo reference frame,
            specified in meters.
        heading_deg: Heading offset of gazebo reference frame, measured
            as angle between       East and gazebo x axis, or
            equivalently, the angle between North and       gazebo y
            axis. The angle is specified in degrees.
        """

        surface_model: str = field(
            default="EARTH_WGS84",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        latitude_deg: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        longitude_deg: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        elevation: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        heading_deg: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
