from dataclasses import dataclass, field
from typing import List, Optional
from .collision import Collision
from .sensor import Sensor
from .visual import Visual

__NAMESPACE__ = "sdformat/v1.0/link.xsd"


@dataclass
class Link:
    class Meta:
        name = "link"

    origin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    damping: Optional["Link.Damping"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    inertial: Optional["Link.Inertial"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    collision: List[Collision] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    visual: List[Visual] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    sensor: Optional[Sensor] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    projector: Optional["Link.Projector"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    gravity: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        }
    )
    self_collide: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )
    kinematic: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class Damping:
        linear: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        angular: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )

    @dataclass
    class Inertial:
        origin: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        inertia: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        mass: float = field(
            default=1.0,
            metadata={
                "type": "Attribute",
            }
        )
        density: float = field(
            default=1.0,
            metadata={
                "type": "Attribute",
            }
        )

    @dataclass
    class Projector:
        texture: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        pose: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            }
        )
        fov: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        near_clip: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        far_clip: Optional[float] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        plugin: List["Link.Projector.Plugin"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )

        @dataclass
        class Plugin:
            any_element: List[object] = field(
                default_factory=list,
                metadata={
                    "type": "Wildcard",
                    "namespace": "##any",
                }
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            filename: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
