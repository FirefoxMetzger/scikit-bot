from dataclasses import dataclass, field
from typing import List, Optional
from .collision import Collision
from .light import Light
from .material import Material
from .sensor import Sensor
from .visual import Visual

__NAMESPACE__ = "sdformat/v1.6/link.xsd"


@dataclass
class Link:
    """A physical link with inertia, collision, and visual properties.

    A link must be a child of a model, and any number of links may exist
    in a model.

    Parameters
    ----------
    gravity: If true, the link is affected by gravity.
    enable_wind: If true, the link is affected by the wind.
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
    light: The light element describes a light source.
    particle_emitter: A particle emitter that can be used to describe
        fog, smoke, and dust.
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
    enable_wind: bool = field(
        default=False,
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
    light: List[Light] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    particle_emitter: List["Link.ParticleEmitter"] = field(
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

    @dataclass
    class ParticleEmitter:
        """
        A particle emitter that can be used to describe fog, smoke, and dust.

        Parameters
        ----------
        emitting: True indicates that the particle emitter should
            generate particles when loaded
        duration: The number of seconds the emitter is active. A value
            less than or equal to zero means infinite duration.
        size: The size of the emitter where the particles are sampled.
            Default value is (1, 1, 1).     Note that the interpretation
            of the emitter area varies     depending on the emmiter
            type:       - point: The area is ignored.       - box: The
            area is interpreted as width X height X depth.       -
            cylinder: The area is interpreted as the bounding box of the
            cylinder. The cylinder is oriented along the Z-axis.       -
            ellipsoid: The area is interpreted as the bounding box of an
            ellipsoid shaped area, i.e. a sphere or
            squashed-sphere area. The parameters are again
            identical to EM_BOX, except that the dimensions
            describe the widest points along each of the axes.
        particle_size: The particle dimensions (width, height, depth).
        lifetime: The number of seconds each particle will ’live’ for
            before being destroyed. This value must be greater than
            zero.
        rate: The number of particles per second that should be emitted.
        min_velocity: Sets a minimum velocity for each particle (m/s).
        max_velocity: Sets a maximum velocity for each particle (m/s).
        scale_rate: Sets the amount by which to scale the particles in
            both x and y direction per second.
        color_start: Sets the starting color for all particles emitted.
            The actual color will be interpolated between this color
            and the one set under color_end.      Color::White is the
            default color for the particles      unless a specific
            function is used.      To specify a color, RGB values should
            be passed in.      For example, to specify red, a user
            should enter:      &amp;lt;color_start&amp;gt;1 0
            0&amp;lt;/color_start&amp;gt;      Note that this function
            overrides the particle colors set      with
            color_range_image.
        color_end: Sets the end color for all particles emitted.     The
            actual color will be interpolated between this color     and
            the one set under color_start.     Color::White is the
            default color for the particles     unless a specific
            function is used (see color_start for     more information
            about defining custom colors with RGB     values).     Note
            that this function overrides the particle colors set
            with color_range_image.
        color_range_image: Sets the path to the color image used as an
            affector. This affector modifies the color of particles in
            flight. The colors are taken from a specified image file.
            The range of color values begins from the left side of the
            image and moves to the right over the lifetime of the
            particle, therefore only the horizontal dimension of the
            image is used.  Note that this function overrides the
            particle colors set with color_start and color_end.
        topic: Topic used to update particle emitter properties at
            runtime.      The default topic is
            /model/{model_name}/particle_emitter/{emitter_name}
            Note that the emitter id and name may not be changed.
        particle_scatter_ratio: This is used to determine the ratio of
            particles that will be detected     by sensors. Increasing
            the ratio means there is a higher chance of     particles
            reflecting and interfering with depth sensing, making the
            emitter appear more dense. Decreasing the ratio decreases
            the chance     of particles reflecting and interfering with
            depth sensing, making it     appear less dense.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the specified frame.
        material: The material of the visual element.
        name: A unique name for the particle emitter.
        type: The type of a particle emitter. One of "box", "cylinder",
            "ellipsoid", or "point".
        """

        emitting: bool = field(
            default=True,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        duration: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        size: str = field(
            default="1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        particle_size: str = field(
            default="1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        lifetime: float = field(
            default=5.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        rate: float = field(
            default=10.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        min_velocity: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        max_velocity: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        scale_rate: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        color_start: str = field(
            default="1 1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
            },
        )
        color_end: str = field(
            default="1 1 1 1",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
            },
        )
        color_range_image: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        topic: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        particle_scatter_ratio: float = field(
            default=0.65,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        pose: Optional["Link.ParticleEmitter.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        material: Optional[Material] = field(
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
        type: Optional[str] = field(
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
