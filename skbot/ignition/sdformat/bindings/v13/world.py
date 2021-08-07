from dataclasses import dataclass, field
from typing import List, Optional
from .actor import Actor
from .joint import Joint
from .light import Light
from .model import Model
from .physics import Physics
from .scene import Scene
from .state import State

__NAMESPACE__ = "sdformat/v1.3/world.xsd"


@dataclass
class World:
    """
    The world element encapsulates an entire world description including:
    models, scene, physics, joints, and plugins.

    Parameters
    ----------
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
    state:
    name: Unique name of the world
    """

    class Meta:
        name = "world"

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
                },
            )
            pose: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "type": "Element",
                    "namespace": "",
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
                    },
                )
                min_dist: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
                max_dist: float = field(
                    default=0.0,
                    metadata={
                        "type": "Element",
                        "namespace": "",
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
