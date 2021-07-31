from dataclasses import dataclass
from .root_type import SdfType


@dataclass
class Sdf(SdfType):
    class Meta:
        name = "sdf"
