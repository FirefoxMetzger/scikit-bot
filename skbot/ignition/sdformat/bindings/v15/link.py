from dataclasses import dataclass, field
from typing import List, Optional
from .collision import Collision
from .sensor import Sensor
from .visual import Visual

__NAMESPACE__ = "sdformat/v1.5/link.xsd"


@dataclass
class Link:
    """A physical link with inertia, collision, and visual properties.

    A link must be a child of a model, and any number of links may exist
    in a model.

    Parameters
    ----------
    gravity: If true, the link is affected by gravity.
    self_collide: If true, the link can collide with other links in the
        model. Two links within a model will collide if
        link1.self_collide OR link2.self_collide. Links connected by a
        joint will never collide.
    kinematic: If true, the link is kinematic only
    must_be_base_link: If true, the link will have 6DOF and be a direct
        child of world.
    velocity_decay: Exponential damping of the link's velocity.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
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
    audio_sink: An audio sink.
    audio_source: An audio source.
    battery: Description of a battery.
    name: A unique name for the link within the scope of the model.
    """

    class Meta:
        name = "link"

    gravity: bool = field(
        default=True,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    self_collide: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    kinematic: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    must_be_base_link: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    velocity_decay: Optional["Link.VelocityDecay"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    frame: List["Link.Frame"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: Optional["Link.Pose"] = field(
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
    sensor: List[Sensor] = field(
        default_factory=list,
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
    audio_sink: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    audio_source: List["Link.AudioSource"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    battery: List["Link.Battery"] = field(
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
                "required": True,
            },
        )
        angular: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
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
            respect to the specified frame.
        name: Name of the frame. This name must not match another frame
            defined inside the parent that this frame is attached to.
        """

        pose: Optional["Link.Frame.Pose"] = field(
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
            frame: Name of frame which the pose is defined relative to.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            frame: Optional[str] = field(
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
        frame: Name of frame which the pose is defined relative to.
        """

        value: str = field(
            default="0 0 0 0 0 0",
            metadata={
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        frame: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class Inertial:
        """
        The inertial properties of the link.

        Parameters
        ----------
        mass: The mass of the link.
        inertia: The 3x3 rotational inertia matrix. Because the
            rotational inertia matrix is symmetric, only 6 above-
            diagonal elements of this matrix are specified here, using
            the attributes ixx, ixy, ixz, iyy, iyz, izz.
        frame: A frame of reference to which a pose is relative.
        pose: This is the pose of the inertial reference frame, relative
            to the specified reference frame. The origin of the inertial
            reference frame needs to be at the center of gravity. The
            axes of the inertial reference frame do not need to be
            aligned with the principal axes of the inertia.
        """

        mass: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        inertia: Optional["Link.Inertial.Inertia"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        frame: List["Link.Inertial.Frame"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: Optional["Link.Inertial.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
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
                    "required": True,
                },
            )
            ixy: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            ixz: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            iyy: float = field(
                default=1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            iyz: float = field(
                default=0.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            izz: float = field(
                default=1.0,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )

        @dataclass
        class Frame:
            """
            A frame of reference to which a pose is relative.

            Parameters
            ----------
            pose: A position(x,y,z) and orientation(roll, pitch yaw)
                with respect to the specified frame.
            name: Name of the frame. This name must not match another
                frame defined inside the parent that this frame is
                attached to.
            """

            pose: Optional["Link.Inertial.Frame.Pose"] = field(
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
                frame: Name of frame which the pose is defined relative
                    to.
                """

                value: str = field(
                    default="0 0 0 0 0 0",
                    metadata={
                        "required": True,
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                frame: Optional[str] = field(
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
            frame: Name of frame which the pose is defined relative to.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            frame: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass
    class Projector:
        """
        Parameters
        ----------
        texture: Texture name
        fov: Field of view
        near_clip: Near clip distance
        far_clip: far clip distance
        frame: A frame of reference to which a pose is relative.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the specified frame.
        plugin: A plugin is a dynamically loaded chunk of code. It can
            exist as a child of world, model, and sensor.
        name: Name of the projector
        """

        texture: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        fov: float = field(
            default=0.785,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        near_clip: float = field(
            default=0.1,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        far_clip: float = field(
            default=10.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        frame: List["Link.Projector.Frame"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: Optional["Link.Projector.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
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
        class Frame:
            """
            A frame of reference to which a pose is relative.

            Parameters
            ----------
            pose: A position(x,y,z) and orientation(roll, pitch yaw)
                with respect to the specified frame.
            name: Name of the frame. This name must not match another
                frame defined inside the parent that this frame is
                attached to.
            """

            pose: Optional["Link.Projector.Frame.Pose"] = field(
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
                frame: Name of frame which the pose is defined relative
                    to.
                """

                value: str = field(
                    default="0 0 0 0 0 0",
                    metadata={
                        "required": True,
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                frame: Optional[str] = field(
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
            frame: Name of frame which the pose is defined relative to.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            frame: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
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

    @dataclass
    class AudioSource:
        """
        An audio source.

        Parameters
        ----------
        uri: URI of the audio media.
        pitch: Pitch for the audio media, in Hz
        gain: Gain for the audio media, in dB.
        contact: List of collision objects that will trigger audio
            playback.
        loop: True to make the audio source loop playback.
        frame: A frame of reference to which a pose is relative.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the specified frame.
        """

        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        pitch: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        gain: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        contact: Optional["Link.AudioSource.Contact"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        loop: bool = field(
            default=False,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        frame: List["Link.AudioSource.Frame"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: Optional["Link.AudioSource.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

        @dataclass
        class Contact:
            """
            List of collision objects that will trigger audio playback.

            Parameters
            ----------
            collision: Name of child collision element that will trigger
                audio playback.
            """

            collision: List[str] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "min_occurs": 1,
                },
            )

        @dataclass
        class Frame:
            """
            A frame of reference to which a pose is relative.

            Parameters
            ----------
            pose: A position(x,y,z) and orientation(roll, pitch yaw)
                with respect to the specified frame.
            name: Name of the frame. This name must not match another
                frame defined inside the parent that this frame is
                attached to.
            """

            pose: Optional["Link.AudioSource.Frame.Pose"] = field(
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
                frame: Name of frame which the pose is defined relative
                    to.
                """

                value: str = field(
                    default="0 0 0 0 0 0",
                    metadata={
                        "required": True,
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    },
                )
                frame: Optional[str] = field(
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
            frame: Name of frame which the pose is defined relative to.
            """

            value: str = field(
                default="0 0 0 0 0 0",
                metadata={
                    "required": True,
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                },
            )
            frame: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass
    class Battery:
        """
        Description of a battery.

        Parameters
        ----------
        voltage: Initial voltage in volts.
        name: Unique name for the battery.
        """

        voltage: float = field(
            default=0.0,
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
