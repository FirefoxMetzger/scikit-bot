from dataclasses import dataclass
from .collision_type import CollisionType


@dataclass
class Collision(CollisionType):
    """The collision properties of a link.

    Note that this can be different from the visual properties of a
    link, for example, simpler collision models are often used to reduce
    computation time.
    """

    class Meta:
        name = "collision"
