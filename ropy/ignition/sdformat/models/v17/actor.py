from dataclasses import dataclass
from .actor_type import ActorType


@dataclass
class Actor(ActorType):
    """A special kind of model which can have a scripted motion.

    This includes both global waypoint type animations and skeleton
    animations.
    """

    class Meta:
        name = "actor"
