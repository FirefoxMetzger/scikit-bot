from dataclasses import dataclass, field
from typing import List, Optional
from .model import Model

__NAMESPACE__ = "sdformat/v1.3/state.xsd"


@dataclass
class State:
    """
    Parameters
    ----------
    sim_time: Simulation time stamp of the state [seconds nanoseconds]
    wall_time: Wall time stamp of the state [seconds nanoseconds]
    real_time: Real time stamp of the state [seconds nanoseconds]
    insertions: A list of new model names
    deletions: A list of deleted model names
    model: Model state
    world_name: Name of the world this state applies to
    """

    class Meta:
        name = "state"

    sim_time: str = field(
        default="0 0",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "white_space": "collapse",
            "pattern": r"\d+ \d+",
        },
    )
    wall_time: str = field(
        default="0 0",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "white_space": "collapse",
            "pattern": r"\d+ \d+",
        },
    )
    real_time: str = field(
        default="0 0",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "white_space": "collapse",
            "pattern": r"\d+ \d+",
        },
    )
    insertions: Optional["State.Insertions"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    deletions: Optional["State.Deletions"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    model: List["State.Model"] = field(
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
        A list of new model names.

        Parameters
        ----------
        model: The model element defines a complete robot or any other
            physical object.
        """

        model: List[Model] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Deletions:
        """
        A list of deleted model names.

        Parameters
        ----------
        name: The name of a deleted model
        """

        name: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )

    @dataclass
    class Model:
        """
        Model state.

        Parameters
        ----------
        pose: Pose of the model
        joint: Joint angle
        link: Link state
        name: Name of the model
        """

        pose: str = field(
            default="0 0 0 0 0 0",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        joint: List["State.Model.Joint"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        link: List["State.Model.Link"] = field(
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
        class Joint:
            """
            Joint angle.

            Parameters
            ----------
            angle: Angle of an axis
            name: Name of the joint
            """

            angle: List["State.Model.Joint.Angle"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "min_occurs": 1,
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
            class Angle:
                """
                Parameters
                ----------
                value:
                axis: Index of the axis.
                """

                value: Optional[float] = field(
                    default=None,
                    metadata={
                        "required": True,
                    },
                )
                axis: Optional[int] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    },
                )

        @dataclass
        class Link:
            """
            Link state.

            Parameters
            ----------
            pose: Pose of the link relative to the model
            velocity: Velocity of the link
            acceleration: Acceleration of the link
            wrench: Force applied to the link
            collision: Collision state
            name: Name of the link
            """

            pose: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            velocity: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            acceleration: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            wrench: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            collision: List["State.Model.Link.Collision"] = field(
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
            class Collision:
                """
                Collision state.

                Parameters
                ----------
                pose: Pose of the link relative to the model
                name: Name of the collision
                """

                pose: str = field(
                    default="0 0 0 0 0 0",
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "required": True,
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                name: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    },
                )
