from dataclasses import dataclass, field
from typing import List, Optional
from .joint import Joint
from .link import Link

__NAMESPACE__ = "sdformat/v1.0/actor.xsd"


@dataclass
class Actor:
    class Meta:
        name = "actor"

    origin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    skin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    animation: List[str] = field(
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
    class Script:
        trajectory: List["Actor.Script.Trajectory"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        loop: bool = field(
            default=True,
            metadata={
                "type": "Attribute",
            },
        )
        delay_start: float = field(
            default=0.0,
            metadata={
                "type": "Attribute",
            },
        )
        auto_start: bool = field(
            default=True,
            metadata={
                "type": "Attribute",
            },
        )

        @dataclass
        class Trajectory:
            waypoint: List[str] = field(
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
    class Plugin:
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
