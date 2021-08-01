from dataclasses import dataclass, field
from typing import List, Optional
from .actor_type import ActorType
from .gui_type import GuiType
from .joint_type import JointType
from .light_type import LightType
from .model_type import ModelType
from .physics_type import PhysicsType
from .plugin_type import PluginType
from .population_type import PopulationType
from .pose_type import PoseType
from .road_type import RoadType
from .scene_type import SceneType
from .spherical_coordinates_type import SphericalCoordinatesType
from .state_type import StateType

__NAMESPACE__ = "sdformat/world"


@dataclass
class WorldType:
    """
    The world element encapsulates an entire world description including:
    models, scene, physics, joints, and plugins.

    Parameters
    ----------
    audio: Global audio properties.
    include: Include resources from a URI
    gui:
    physics: The physics tag specifies the type and properties of the
        dynamics engine.
    scene: Specifies the look of the environment.
    light: The light element describes a light source.
    model: The model element defines a complete robot or any other
        physical object.
    actor:
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    joint: A joint connections two links with kinematic and dynamic
        properties.
    road:
    spherical_coordinates:
    state:
    population: The population element defines how and where a set of
        models will be automatically populated in Gazebo.
    name: Unique name of the world
    """

    class Meta:
        name = "worldType"

    audio: List["WorldType.Audio"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    include: List["WorldType.Include"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gui: List[GuiType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    physics: List[PhysicsType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    scene: List[SceneType] = field(
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
    model: List[ModelType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    actor: List[ActorType] = field(
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
    joint: List[JointType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    road: List[RoadType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    spherical_coordinates: List[SphericalCoordinatesType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    state: List[StateType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    population: List[PopulationType] = field(
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
    class Audio:
        """
        Global audio properties.

        Parameters
        ----------
        device: Device to use for audio playback. A value of "default"
            will use the system's default audio device. Otherwise,
            specify a an audio device file"
        """

        device: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

    @dataclass
    class Include:
        """
        Include resources from a URI.

        Parameters
        ----------
        uri: URI to a resource, such as a model
        name: Override the name of the included model.
        static: Override the static value of the included model.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the specified frame.
        """

        uri: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
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
        pose: List[PoseType] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
