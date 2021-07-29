from dataclasses import dataclass
from .noise_type import NoiseType


@dataclass
class Noise(NoiseType):
    """
    The properties of a sensor noise model.
    """
    class Meta:
        name = "noise"
