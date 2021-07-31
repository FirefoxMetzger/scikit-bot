from dataclasses import dataclass, field
from typing import List, Optional
from .actor_type import ActorType
from .light_type import LightType
from .model_type import ModelType
from .world_type import WorldType

__NAMESPACE__ = "sdformat/root"


@dataclass
class SdfType:
    """SDFormat base element that can include 0-N models, actors, lights,
    and/or worlds.

    A user of multiple worlds could run parallel instances of
    simulation, or offer selection of a world at runtime.

    Parameters
    ----------
    world: The world element encapsulates an entire world description
        including: models, scene, physics, joints, and plugins.
    model: The model element defines a complete robot or any other
        physical object.
    actor: A special kind of model which can have a scripted motion.
        This includes both global waypoint type animations and skeleton
        animations.
    light: The light element describes a light source.
    version: Version number of the SDFormat specification.
    """
    class Meta:
        name = "sdfType"

    world: List[WorldType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    model: List[ModelType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    actor: List[ActorType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    light: List[LightType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
