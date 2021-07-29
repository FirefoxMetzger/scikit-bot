from dataclasses import dataclass
from .box_shape_type import BoxType


@dataclass
class Box(BoxType):
    """
    Box shape.
    """
    class Meta:
        name = "box"
