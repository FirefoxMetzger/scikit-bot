from dataclasses import dataclass, field
from typing import List, Optional
from .actor_type import ActorType
from .atmosphere_type import AtmosphereType
from .frame_type import FrameType
from .gui_type import GuiType
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
    models, scene, physics, and plugins.

    Parameters
    ----------
    audio: Global audio properties.
    wind: The wind tag specifies the type and properties of the wind.
    include: Include resources from a URI
    gravity: The gravity vector in m/s^2, expressed in a coordinate
        frame defined by the spherical_coordinates tag.
    magnetic_field: The magnetic vector in Tesla, expressed in a
        coordinate frame defined by the spherical_coordinates tag.
    atmosphere: The atmosphere tag specifies the type and properties of
        the atmosphere model.
    gui:
    physics: The physics tag specifies the type and properties of the
        dynamics engine.
    scene: Specifies the look of the environment.
    light: The light element describes a light source.
    frame: A frame of reference to which a pose is relative.
    model: The model element defines a complete robot or any other
        physical object.
    actor: A special kind of model which can have a scripted motion.
        This includes both global waypoint type animations and skeleton
        animations.
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
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
        }
    )
    wind: List["WorldType.Wind"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    include: List["WorldType.Include"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    gravity: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        }
    )
    magnetic_field: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        }
    )
    atmosphere: List[AtmosphereType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    gui: List[GuiType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    physics: List[PhysicsType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    scene: List[SceneType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    light: List[LightType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    frame: List[FrameType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    model: List[ModelType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    actor: List[ActorType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    plugin: List[PluginType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    road: List[RoadType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    spherical_coordinates: List[SphericalCoordinatesType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    state: List[StateType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    population: List[PopulationType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
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
            }
        )

    @dataclass
    class Wind:
        """
        The wind tag specifies the type and properties of the wind.

        Parameters
        ----------
        linear_velocity: Linear velocity of the wind.
        """
        linear_velocity: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            }
        )

    @dataclass
    class Include:
        """
        Include resources from a URI.

        Parameters
        ----------
        uri: URI to a resource, such as a model
        name: Override the name of the included entity.
        static: Override the static value of the included entity.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the frame named in the relative_to attribute.
        """
        uri: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        name: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        static: List[bool] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        pose: List[PoseType] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
