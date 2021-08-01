from dataclasses import dataclass
from .physics_type import PhysicsType


@dataclass
class Physics(PhysicsType):
    class Meta:
        name = "physics"
