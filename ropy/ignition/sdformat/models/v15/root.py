from dataclasses import dataclass
from .root_type import SdfType


@dataclass
class Sdf(SdfType):
    """
    SDFormat base element.
    """
    class Meta:
        name = "sdf"
