from dataclasses import dataclass
from .collision_type import CollisionType


@dataclass
class Collision(CollisionType):
    class Meta:
        name = "collision"
