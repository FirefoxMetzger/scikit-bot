from dataclasses import dataclass
from .physics_type import PhysicsType


@dataclass
class Physics(PhysicsType):
    """
    The physics tag specifies the type and properties of the dynamics engine.
    """
    class Meta:
        name = "physics"
