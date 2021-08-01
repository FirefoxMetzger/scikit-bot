from dataclasses import dataclass, field
from typing import List, Optional
from .frame_type import FrameType
from .link_state_type import LinkType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/model_state"


@dataclass
class ModelType:
    """
    Model state.

    Parameters
    ----------
    joint: Joint angle
    model: A nested model state element
    scale: Scale for the 3 dimensions of the model.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    link: Link state
    name: Name of the model
    """

    class Meta:
        name = "modelType"

    joint: List["ModelType.Joint"] = field(
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
    scale: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
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
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Joint:
        """
        Joint angle.

        Parameters
        ----------
        angle: Angle of an axis
        name: Name of the joint
        """

        angle: List["ModelType.Joint.Angle"] = field(
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
        class Angle:
            """
            Angle of an axis.

            Parameters
            ----------
            value:
            axis: Index of the axis.
            """

            value: Optional[float] = field(
                default=None,
                metadata={
                    "required": True,
                },
            )
            axis: Optional[int] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
