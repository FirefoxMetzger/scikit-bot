from dataclasses import dataclass, field
from typing import List, Optional
from .actor import Actor
from .light import Light
from .model import Model
from .world import World

__NAMESPACE__ = "sdformat/v1.7/sdf.xsd"


@dataclass
class Sdf:
    """SDFormat base element that can include 0-N models, actors, lights,
    and/or worlds.

    A user of multiple worlds could run parallel instances of
    simulation, or offer selection of a world at runtime.

    Parameters
    ----------
    world: The world element encapsulates an entire world description
        including: models, scene, physics, and plugins.
    model: The model element defines a complete robot or any other
        physical object.
    actor: A special kind of model which can have a scripted motion.
        This includes both global waypoint type animations and skeleton
        animations.
    light: The light element describes a light source.
    version: Version number of the SDFormat specification.
    """

    class Meta:
        name = "sdf"

    world: List[World] = field(
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
    light: List[Light] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
