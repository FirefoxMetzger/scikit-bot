from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .gripper_type import GripperType
from .joint_type import JointType
from .link_type import LinkType
from .plugin_type import PluginType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/model"


@dataclass
class ModelType:
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
        models.
    model: A nested model element
    enable_wind: If set to true, all links in the model will be affected
        by the wind. Can be overriden by the link wind property.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
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
    """

    class Meta:
        name = "modelType"

    static: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    self_collide: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    allow_auto_disable: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    include: List["ModelType.Include"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    model: List["ModelType"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    enable_wind: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    frame: List[FrameType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: List[PoseType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    link: List[LinkType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    joint: List[JointType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    plugin: List[PluginType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gripper: List[GripperType] = field(
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
    class Include:
        """Include resources from a URI.

        This can be used to nest models.

        Parameters
        ----------
        uri: URI to a resource, such as a model
        pose: Override the pose of the included model. A position and
            orientation in the global coordinate frame for the model.
            Position(x,y,z) and rotation (roll, pitch yaw) in the global
            coordinate frame.
        name: Override the name of the included model.
        static: Override the static value of the included model.
        """

        uri: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        pose: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        name: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        static: List[bool] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
