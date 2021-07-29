from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .plugin_type import PluginType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/gui"


@dataclass
class GuiType:
    """
    Parameters
    ----------
    camera:
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    fullscreen:
    """
    class Meta:
        name = "guiType"

    camera: List["GuiType.Camera"] = field(
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
    fullscreen: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class Camera:
        """
        Parameters
        ----------
        view_controller:
        projection_type: Set the type of projection for the camera.
            Valid values are "perspective" and "orthographic".
        track_visual:
        frame: A frame of reference to which a pose is relative.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect to the specified frame.
        name:
        """
        view_controller: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        projection_type: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
        track_visual: List["GuiType.Camera.TrackVisual"] = field(
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
        pose: List[PoseType] = field(
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
        class TrackVisual:
            """
            Parameters
            ----------
            name: Name of the tracked visual. If no name is provided,
                the remaining settings will be applied whenever tracking
                is triggered in the GUI.
            min_dist: Minimum distance between the camera and the
                tracked visual. This parameter is only used if static is
                set to false.
            max_dist: Maximum distance between the camera and the
                tracked visual. This parameter is only used if static is
                set to false.
            static: If set to true, the position of the camera is fixed
                relatively to the model or to the world, depending on
                the value of the use_model_frame element. Otherwise, the
                position of the camera may vary but the distance between
                the camera and the model will depend on the value of the
                min_dist and max_dist elements. In any case, the camera
                will always follow the model by changing its
                orientation.
            use_model_frame: If set to true, the position of the camera
                is relative to the model reference frame, which means
                that its position relative to the model will not change.
                Otherwise, the position of the camera is relative to the
                world reference frame, which means that its position
                relative to the world will not change. This parameter is
                only used if static is set to true.
            xyz: The position of the camera's reference frame. This
                parameter is only used if static is set to true. If
                use_model_frame is set to true, the position is relative
                to the model reference frame, otherwise it represents
                world coordinates.
            inherit_yaw: If set to true, the camera will inherit the yaw
                rotation of the tracked model. This parameter is only
                used if static and use_model_frame are set to true.
            """
            name: List[str] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            min_dist: List[float] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            max_dist: List[float] = field(
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
            use_model_frame: List[bool] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
            xyz: List[str] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
                }
            )
            inherit_yaw: List[bool] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "namespace": "",
                }
            )
