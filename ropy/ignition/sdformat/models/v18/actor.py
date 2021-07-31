from dataclasses import dataclass
from .actor_type import ActorType


@dataclass
class Actor(ActorType):
    class Meta:
        name = "actor"
