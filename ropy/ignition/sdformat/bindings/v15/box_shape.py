from dataclasses import dataclass
from .box_shape_type import BoxType


@dataclass
class Box(BoxType):
    class Meta:
        name = "box"
