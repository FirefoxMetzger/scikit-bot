from dataclasses import dataclass
from .world_type import WorldType


@dataclass
class World(WorldType):
    """
    The world element encapsulates an entire world description including:
    models, scene, physics, joints, and plugins.
    """

    class Meta:
        name = "world"
