from dataclasses import dataclass
from .sphere_shape_type import SphereType


@dataclass
class Sphere(SphereType):
    """
    Sphere shape.
    """

    class Meta:
        name = "sphere"
