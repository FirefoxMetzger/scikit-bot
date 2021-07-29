from dataclasses import dataclass
from .ray_type import RayType


@dataclass
class Ray(RayType):
    """
    These elements are specific to the ray (laser) sensor.
    """
    class Meta:
        name = "ray"
