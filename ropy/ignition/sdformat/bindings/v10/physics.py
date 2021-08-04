from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/v1.0/physics.xsd"


@dataclass
class Physics:
    class Meta:
        name = "physics"

    max_contacts: int = field(
        default=20,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gravity: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    bullet: Optional["Physics.Bullet"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    ode: Optional["Physics.Ode"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    update_rate: float = field(
        default=0.0,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class Bullet:
        dt: float = field(
            default=0.003,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Ode:
        solver: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        constraints: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
