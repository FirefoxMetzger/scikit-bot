from dataclasses import dataclass, field
from typing import List, Optional
from .actor import Actor
from .light import Light
from .model import Model
from .world import World

__NAMESPACE__ = "sdformat/v1.5/sdf.xsd"


@dataclass
class Sdf:
    """
    SDFormat base element.

    Parameters
    ----------
    world: The world element encapsulates an entire world description
        including: models, scene, physics, joints, and plugins
    model: The model element defines a complete robot or any other
        physical object.
    actor:
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
