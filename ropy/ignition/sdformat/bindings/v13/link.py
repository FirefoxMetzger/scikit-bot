from dataclasses import dataclass, field
from typing import List, Optional
from .collision import Collision
from .sensor import Sensor
from .visual import Visual

__NAMESPACE__ = "sdformat/v1.3/link.xsd"


@dataclass
class Link:
    """A physical link with inertia, collision, and visual properties.

    A link must be a child of a model, and any number of links may exist
    in a model.

    Parameters
    ----------
    gravity: If true, the link is affected by gravity.
    self_collide: If true, the link can collide with other links in the
        model.
    kinematic: If true, the link is kinematic only
    pose: This is the pose of the link reference frame, relative to the
        model reference frame.
    velocity_decay: Exponential damping of the link's velocity.
    inertial: The inertial properties of the link.
    collision: The collision properties of a link. Note that this can be
        different from the visual properties of a link, for example,
        simpler collision models are often used to reduce computation
        time.
    visual: The visual properties of the link. This element specifies
        the shape of the object (box, cylinder, etc.) for visualization
        purposes.
    sensor: The sensor tag describes the type and properties of a
        sensor.
    projector:
    name: A unique name for the link within the scope of the model.
    """

    class Meta:
        name = "link"

    gravity: bool = field(
        default=True,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    self_collide: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    kinematic: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: str = field(
        default="0 0 0 0 0 0",
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    velocity_decay: Optional["Link.VelocityDecay"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    inertial: Optional["Link.Inertial"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    collision: List[Collision] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    visual: List[Visual] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    sensor: Optional[Sensor] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    projector: Optional["Link.Projector"] = field(
        default=None,
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
    class VelocityDecay:
        """
        Exponential damping of the link's velocity.

        Parameters
        ----------
        linear: Linear damping
        angular: Angular damping
        """

        linear: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        angular: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Inertial:
        """
        The inertial properties of the link.

        Parameters
        ----------
        mass: The mass of the link.
        pose: This is the pose of the inertial reference frame, relative
            to the link reference frame. The origin of the inertial
            reference frame needs to be at the center of gravity. The
            axes of the inertial reference frame do not need to be
            aligned with the principal axes of the inertia.
        inertia: The 3x3 rotational inertia matrix. Because the
            rotational inertia matrix is symmetric, only 6 above-
            diagonal elements of this matrix are specified here, using
            the attributes ixx, ixy, ixz, iyy, iyz, izz.
        """

        mass: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: str = field(
            default="0 0 0 0 0 0",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        inertia: Optional["Link.Inertial.Inertia"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Inertia:
            """The 3x3 rotational inertia matrix.

            Because the rotational inertia matrix is symmetric, only 6
            above-diagonal elements of this matrix are specified here,
            using the attributes ixx, ixy, ixz, iyy, iyz, izz.
            """

            ixx: float = field(
                default=1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            ixy: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            ixz: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            iyy: float = field(
                default=1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            iyz: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            izz: float = field(
                default=1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Projector:
        """
        Parameters
        ----------
        texture: Texture name
        pose: Pose of the projector
        fov: Field of view
        near_clip: Near clip distance
        far_clip: far clip distance
        plugin: A plugin is a dynamically loaded chunk of code. It can
            exist as a child of world, model, and sensor.
        name: Name of the projector
        """

        texture: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: str = field(
            default="0 0 0 0 0 0",
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        fov: float = field(
            default=0.785,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        near_clip: float = field(
            default=0.1,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        far_clip: float = field(
            default=10.0,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        plugin: List["Link.Projector.Plugin"] = field(
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
        class Plugin:
            """A plugin is a dynamically loaded chunk of code.

            It can exist as a child of world, model, and sensor.

            Parameters
            ----------
            any_element: This is a special element that should not be
                specified in an SDFormat file. It automatically copies
                child elements into the SDFormat element so that a
                plugin can access the data.
            name: A unique name for the plugin, scoped to its parent.
            filename: Name of the shared library to load. If the
                filename is not a full path name, the file will be
                searched for in the configuration paths.
            """

            any_element: List[object] = field(
                default_factory=list,
                metadata={
                    "type": "Wildcard",
                    "namespace": "##any",
                },
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
            filename: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
