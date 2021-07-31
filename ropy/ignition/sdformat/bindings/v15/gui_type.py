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
