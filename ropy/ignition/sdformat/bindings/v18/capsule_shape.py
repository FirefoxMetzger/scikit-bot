from dataclasses import dataclass
from .capsule_shape_type import CapsuleType


@dataclass
class Capsule(CapsuleType):
    class Meta:
        name = "capsule"
