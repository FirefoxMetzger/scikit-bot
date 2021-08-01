from dataclasses import dataclass
from .ray_type import RayType


@dataclass
class Ray(RayType):
    class Meta:
        name = "ray"
