from dataclasses import dataclass
from .root_type import SdfType


@dataclass
class Sdf(SdfType):
    """SDFormat base element that can include 0-N models, actors, lights,
    and/or worlds.

    A user of multiple worlds could run parallel instances of
    simulation, or offer selection of a world at runtime.
    """
    class Meta:
        name = "sdf"
