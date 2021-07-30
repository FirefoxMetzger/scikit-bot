from dataclasses import dataclass
from .light_type import LightType


@dataclass
class Light(LightType):
    """
    The light element describes a light source.
    """

    class Meta:
        name = "light"
