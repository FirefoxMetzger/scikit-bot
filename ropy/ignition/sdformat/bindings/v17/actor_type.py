from dataclasses import dataclass, field
from typing import List, Optional
from .joint_type import JointType
from .link_type import LinkType
from .plugin_type import PluginType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/actor"


@dataclass
class ActorType:
    """A special kind of model which can have a scripted motion.

    This includes both global waypoint type animations and skeleton
    animations.

    Parameters
    ----------
    skin: Skin file which defines a visual and the underlying skeleton
        which moves it.
    animation: Animation file defines an animation for the skeleton in
        the skin. The skeleton must be compatible with the skin
        skeleton.
    script: Adds scripted trajectories to the actor.
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
    name: A unique name for the actor.
    """
    class Meta:
        name = "actorType"

    skin: List["ActorType.Skin"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    animation: List["ActorType.Animation"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    script: List["ActorType.Script"] = field(
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
    link: List[LinkType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    joint: List[JointType] = field(
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

    @dataclass
    class Skin:
        """
        Skin file which defines a visual and the underlying skeleton which
        moves it.

        Parameters
        ----------
        filename: Path to skin file, accepted formats: COLLADA, BVH.
        scale: Scale the skin's size.
        """
        filename: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        scale: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Animation:
        """Animation file defines an animation for the skeleton in the skin.

        The skeleton must be compatible with the skin skeleton.

        Parameters
        ----------
        filename: Path to animation file. Accepted formats: COLLADA,
            BVH.
        scale: Scale for the animation skeleton.
        interpolate_x: Set to true so the animation is interpolated on
            X.
        name: Unique name for animation.
        """
        filename: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        scale: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        interpolate_x: List[bool] = field(
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
    class Script:
        """
        Adds scripted trajectories to the actor.

        Parameters
        ----------
        loop: Set this to true for the script to be repeated in a loop.
            For a fluid continuous motion, make sure the last waypoint
            matches the first one.
        delay_start: This is the time to wait before starting the
            script. If running in a loop, this time will be waited
            before starting each cycle.
        auto_start: Set to true if the animation should start as soon as
            the simulation starts playing. It is useful to set this to
            false if the animation should only start playing only when
            triggered by a plugin, for example.
        trajectory: The trajectory contains a series of keyframes to be
            followed.
        """
        loop: List[bool] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        delay_start: List[float] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        auto_start: List[bool] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        trajectory: List["ActorType.Script.Trajectory"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

        @dataclass
        class Trajectory:
            """
            The trajectory contains a series of keyframes to be followed.

            Parameters
            ----------
            waypoint: Each point in the trajectory.
            id: Unique id for a trajectory.
            type: If it matches the type of an animation, they will be
                played at the same time.
            tension: The tension of the trajectory spline. The default
                value of zero equates to a Catmull-Rom spline, which may
                also cause the animation to overshoot keyframes. A value
                of one will cause the animation to stick to the
                keyframes.
            """
            waypoint: List["ActorType.Script.Trajectory.Waypoint"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            id: Optional[int] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            type: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            tension: float = field(
                default=0.0,
                metadata={
                    "type": "Attribute",
                }
            )

            @dataclass
            class Waypoint:
                """
                Each point in the trajectory.

                Parameters
                ----------
                time: The time in seconds, counted from the beginning of
                    the script, when the pose should be reached.
                pose: The pose which should be reached at the given
                    time.
                """
                time: List[float] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    }
                )
                pose: List[str] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                        "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                    }
                )