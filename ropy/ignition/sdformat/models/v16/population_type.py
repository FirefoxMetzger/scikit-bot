from dataclasses import dataclass, field
from typing import List, Optional
from .box_shape_type import BoxType
from .cylinder_shape_type import CylinderType
from .frame_type import FrameType
from .model_type import ModelType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/population"


@dataclass
class PopulationType:
    """
    Parameters
    ----------
    model_count: The number of models to place.
    distribution: Specifies the type of object distribution and its
        optional parameters.
    box: Box shape
    cylinder: Cylinder shape
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    model: The model element defines a complete robot or any other
        physical object.
    name: A unique name for the population. This name must not match
        another population in the world.
    """

    class Meta:
        name = "populationType"

    model_count: List[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    distribution: List["PopulationType.Distribution"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    box: List[BoxType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    cylinder: List[CylinderType] = field(
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
    model: List[ModelType] = field(
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
    class Distribution:
        """
        Parameters
        ----------
        type: Define how the objects will be placed in the specified
            region. - random: Models placed at random. - uniform: Models
            approximately placed in a 2D grid pattern with control over
            the number of objects. - grid: Models evenly placed in a 2D
            grid pattern. The number of objects is not explicitly
            specified, it is based on the number of rows and columns of
            the grid. - linear-x: Models evently placed in a row along
            the global x-axis. - linear-y: Models evently placed in a
            row along the global y-axis. - linear-z: Models evently
            placed in a row along the global z-axis.
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        step: Distance between elements of the grid.
        """

        type: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        rows: List[int] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        cols: List[int] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        step: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
