from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/v1.0/joint.xsd"


@dataclass
class Joint:
    class Meta:
        name = "joint"

    parent: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    child: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    origin: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    thread_pitch: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    axis: Optional["Joint.Axis"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    axis2: Optional["Joint.Axis2"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    physics: Optional["Joint.Physics"] = field(
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
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

    @dataclass
    class Axis:
        dynamics: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        limit: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        xyz: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            }
        )

    @dataclass
    class Axis2:
        dynamics: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        limit: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        xyz: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            }
        )

    @dataclass
    class Physics:
        ode: Optional["Joint.Physics.Ode"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

        @dataclass
        class Ode:
            fudge_factor: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            cfm: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            bounce: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            max_force: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            velocity: Optional[float] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            limit: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            suspension: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
