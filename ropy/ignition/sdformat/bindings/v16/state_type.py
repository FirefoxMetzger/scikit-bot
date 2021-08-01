from dataclasses import dataclass, field
from typing import List, Optional
from .light_state_type import LightType
from .light_type import LightType as LightTypeLightType
from .model_state_type import ModelType
from .model_type import ModelType as ModelTypeModelType

__NAMESPACE__ = "sdformat/state"


@dataclass
class StateType:
    """
    Parameters
    ----------
    sim_time: Simulation time stamp of the state [seconds nanoseconds]
    wall_time: Wall time stamp of the state [seconds nanoseconds]
    real_time: Real time stamp of the state [seconds nanoseconds]
    iterations: Number of simulation iterations.
    insertions: A list containing the entire description of entities
        inserted.
    deletions: A list of names of deleted entities/
    model: Model state
    light: Light state
    world_name: Name of the world this state applies to
    """

    class Meta:
        name = "stateType"

    sim_time: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"\d+ \d+",
        },
    )
    wall_time: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"\d+ \d+",
        },
    )
    real_time: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"\d+ \d+",
        },
    )
    iterations: List[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    insertions: List["StateType.Insertions"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    deletions: List["StateType.Deletions"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    model: List[ModelType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    light: List[LightType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    world_name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Insertions:
        """
        A list containing the entire description of entities inserted.

        Parameters
        ----------
        model: The model element defines a complete robot or any other
            physical object.
        light: The light element describes a light source.
        """

        model: List[ModelTypeModelType] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        light: List[LightTypeLightType] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Deletions:
        """
        A list of names of deleted entities/

        Parameters
        ----------
        name: The name of a deleted entity.
        """

        name: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
