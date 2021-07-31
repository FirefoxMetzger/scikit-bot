from dataclasses import dataclass
from .sphere_shape_type import SphereType


@dataclass
class Sphere(SphereType):
    class Meta:
        name = "sphere"
