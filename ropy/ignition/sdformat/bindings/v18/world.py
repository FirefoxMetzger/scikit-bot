from dataclasses import dataclass
from .world_type import WorldType


@dataclass
class World(WorldType):
    class Meta:
        name = "world"
