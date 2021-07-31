from dataclasses import dataclass
from .light_type import LightType


@dataclass
class Light(LightType):
    class Meta:
        name = "light"
