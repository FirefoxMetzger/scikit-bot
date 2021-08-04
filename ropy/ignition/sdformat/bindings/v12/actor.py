from dataclasses import dataclass, field
from typing import List, Optional
from .joint import Joint
from .link import Link

__NAMESPACE__ = "sdformat/v1.2/actor.xsd"


@dataclass
class Actor:
    """
    Parameters
    ----------
    pose: Origin of the actor
    skin:
    animation:
    script:
    link: A physical link with inertia, collision, and visual
        properties. A link must be a child of a model, and any number of
        links may exist in a model.
    joint: A joint connections two links with kinematic and dynamic
        properties.
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    name:
    static:
    """

    class Meta:
        name = "actor"

    pose: str = field(
        default="0 0 0 0 0 0",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    skin: Optional["Actor.Skin"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    animation: List["Actor.Animation"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    script: Optional["Actor.Script"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    link: List[Link] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    joint: List[Joint] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    plugin: List["Actor.Plugin"] = field(
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
    static: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class Skin:
        filename: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        scale: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Animation:
        filename: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        scale: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        interpolate_x: bool = field(
            default=False,
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
    class Script:
        loop: bool = field(
            default=True,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        delay_start: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        auto_start: bool = field(
            default=True,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        trajectory: List["Actor.Script.Trajectory"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Trajectory:
            waypoint: List["Actor.Script.Trajectory.Waypoint"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            id: Optional[int] = field(
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
            class Waypoint:
                time: float = field(
                    default=0.0,
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
