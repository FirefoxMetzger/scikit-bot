from dataclasses import dataclass, field
from typing import List, Optional
from .joint import Joint
from .link import Link

__NAMESPACE__ = "sdformat/v1.8/model.xsd"


@dataclass
class Model:
    """
    The model element defines a complete robot or any other physical object.

    Parameters
    ----------
    static: If set to true, the model is immovable. Otherwise the model
        is simulated in the dynamics engine.
    self_collide: If set to true, all links in the model will collide
        with each other (except those connected by a joint). Can be
        overridden by the link or collision element self_collide
        property. Two links within a model will collide if
        link1.self_collide OR link2.self_collide. Links connected by a
        joint will never collide.
    allow_auto_disable: Allows a model to auto-disable, which is means
        the physics engine can skip updating the model when the model is
        at rest. This parameter is only used by models with no joints.
    include: Include resources from a URI. This can be used to nest
        models. Included resources can only contain one 'model', 'light'
        or 'actor' element. The URI can point to a directory or a file.
        If the URI is a directory, it must conform to the model database
        structure (see
        /tutorials?tut=composition&amp;cat=specification&amp;#defining-
        models-in-separate-files).
    model: A nested model element
    enable_wind: If set to true, all links in the model will be affected
        by the wind. Can be overriden by the link wind property.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
    link: A physical link with inertia, collision, and visual
        properties. A link must be a child of a model, and any number of
        links may exist in a model.
    joint: A joint connects two links with kinematic and dynamic
        properties. By default, the pose of a joint is expressed in the
        child link frame.
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    gripper:
    name: A unique name for the model. This name must not match another
        model in the world.
    canonical_link: The name of the model's canonical link, to which the
        model's implicit       coordinate frame is attached. If unset or
        set to an empty string,       the first link element listed as a
        child of this model is chosen       as the canonical link.
    placement_frame: The frame inside this model whose pose will be set
        by the pose element of the model. i.e, the pose element
        specifies the pose of this frame instead of the model frame.
    """

    class Meta:
        name = "model"

    static: bool = field(
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
    allow_auto_disable: bool = field(
        default=True,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    include: List["Model.Include"] = field(
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
    enable_wind: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
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
    link: List[Link] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    joint: List[Joint] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    plugin: List["Model.Plugin"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gripper: List["Model.Gripper"] = field(
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
    canonical_link: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    placement_frame: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class Include:
        """Include resources from a URI.

        This can be used to nest models. Included resources can only contain one 'model', 'light' or 'actor' element. The URI can point to a directory or a file. If the URI is a directory, it must conform to the model database structure (see /tutorials?tut=composition&amp;cat=specification&amp;#defining-models-in-separate-files).

        Parameters
        ----------
        uri: URI to a resource, such as a model
        name: Override the name of the included model.
        static: Override the static value of the included model.
        placement_frame: The frame inside the included model whose pose
            will be set by the specified pose element. If this element
            is specified, the pose must be specified.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the frame named in the relative_to attribute.
        """

        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        static: bool = field(
            default=False,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        placement_frame: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: Optional["Model.Include.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
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
    class Plugin:
        """A plugin is a dynamically loaded chunk of code.

        It can exist as a child of world, model, and sensor.

        Parameters
        ----------
        any_element: This is a special element that should not be
            specified in an SDFormat file. It automatically copies child
            elements into the SDFormat element so that a plugin can
            access the data.
        name: A unique name for the plugin, scoped to its parent.
        filename: Name of the shared library to load. If the filename is
            not a full path name, the file will be searched for in the
            configuration paths.
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
    class Gripper:
        grasp_check: Optional["Model.Gripper.GraspCheck"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        gripper_link: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )
        palm_link: str = field(
            default="__default__",
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
        class GraspCheck:
            detach_steps: int = field(
                default=40,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            attach_steps: int = field(
                default=20,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            min_contact_count: int = field(
                default=2,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
