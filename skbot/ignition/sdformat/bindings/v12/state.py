from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/v1.2/state.xsd"


@dataclass
class State:
    """
    Parameters
    ----------
    time: Time stamp of the state [seconds nanoseconds]
    model: Model state
    world_name: Name of the world this state applies to
    """

    class Meta:
        name = "state"

    time: float = field(
        default="0 0",
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
            "min_occurs": 1,
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
    class Model:
        """
        Model state.

        Parameters
        ----------
        pose: Pose of the model
        link: Link state
        name: Name of the model
        """

        pose: str = field(
            default="0 0 0 0 0 0",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
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
        class Link:
            """
            Link state.

            Parameters
            ----------
            pose: Pose of the link relative to the model
            velocity: Velocity of the link
            wrench: Force applied to the link
            name: Name of the link
            """

            pose: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            velocity: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            wrench: List["State.Model.Link.Wrench"] = field(
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
            class Wrench:
                """
                Force applied to the link.

                Parameters
                ----------
                pos: Position of the force.
                mag: Magnitude of the force.
                """

                pos: str = field(
                    default="0 0 0",
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                mag: str = field(
                    default="0 0 0 0 0 0",
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
