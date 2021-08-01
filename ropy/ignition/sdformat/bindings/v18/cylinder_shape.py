from dataclasses import dataclass
from .cylinder_shape_type import CylinderType


@dataclass
class Cylinder(CylinderType):
    class Meta:
        name = "cylinder"
