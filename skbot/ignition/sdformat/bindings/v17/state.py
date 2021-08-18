from dataclasses import dataclass, field
from typing import List, Optional
from .light import Light
from .model import Model as ModelModel

__NAMESPACE__ = "sdformat/v1.7/state.xsd"


@dataclass
class Model:
    """
    Model state.

    Parameters
    ----------
    joint: Joint angle
    model: A nested model state element
    scale: Scale for the 3 dimensions of the model.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
    link: Link state
    name: Name of the model
    """

    class Meta:
        name = "model"

    joint: List["Model.Joint"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    model: List["Model"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    scale: str = field(
        default="1 1 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    frame: List["Model.Frame"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: Optional["Model.Pose"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    link: List["Model.Link"] = field(
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

        angle: List["Model.Joint.Angle"] = field(
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
    class Frame:
        """
        A frame of reference to which a pose is relative.

        Parameters
        ----------
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the frame named in the relative_to attribute.
        name: Name of the frame. This name must not match another frame
            defined inside the parent that this frame is attached to.
        attached_to: Name of the link or frame to which this frame is
            attached.       If a frame is specified, recursively
            following the attached_to attributes       of the specified
            frames must lead to the name of a link, a model, or the
            world frame.
        """

        pose: Optional["Model.Frame.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        attached_to: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

        @dataclass
        class Pose:
            """
            Parameters
            ----------
            value:
            relative_to: Name of frame relative to which the pose is
                applied.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            relative_to: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass
    class Pose:
        """
        Parameters
        ----------
        value:
        relative_to: Name of frame relative to which the pose is
            applied.
        """

        value: str = field(
            default="0 0 0 0 0 0",
            metadata={
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        relative_to: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class Link:
        """
        Link state.

        Parameters
        ----------
        velocity: Velocity of the link. The x, y, z components of the
            pose       correspond to the linear velocity of the link,
            and the roll, pitch, yaw       components correspond to the
            angular velocity of the link
        acceleration: Acceleration of the link. The x, y, z components
            of the pose       correspond to the linear acceleration of
            the link, and the roll,       pitch, yaw components
            correspond to the angular acceleration of the link
        wrench: Force and torque applied to the link. The x, y, z
            components       of the pose correspond to the force applied
            to the link, and the roll,       pitch, yaw components
            correspond to the torque applied to the link
        collision: Collision state
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the frame named in the relative_to attribute.
        name: Name of the link
        """

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
        collision: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: Optional["Model.Link.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
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
        class Pose:
            """
            Parameters
            ----------
            value:
            relative_to: Name of frame relative to which the pose is
                applied.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            relative_to: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )


@dataclass
class State:
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
    iterations: int = field(
        default=0,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
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
    model: List[Model] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    light: List["State.Light"] = field(
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

        model: List[ModelModel] = field(
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
                "min_occurs": 1,
            },
        )

    @dataclass
    class Light:
        """
        Light state.

        Parameters
        ----------
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the frame named in the relative_to attribute.
        name: Name of the light
        """

        pose: Optional["State.Light.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
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
        class Pose:
            """
            Parameters
            ----------
            value:
            relative_to: Name of frame relative to which the pose is
                applied.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            relative_to: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
