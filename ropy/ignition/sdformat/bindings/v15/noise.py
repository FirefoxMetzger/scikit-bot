from dataclasses import dataclass
from .noise_type import NoiseType


@dataclass
class Noise(NoiseType):
    class Meta:
        name = "noise"
