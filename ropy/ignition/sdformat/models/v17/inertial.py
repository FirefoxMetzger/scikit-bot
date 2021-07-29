from dataclasses import dataclass
from .inertial_type import InertialType


@dataclass
class Inertial(InertialType):
    """
    The inertial properties of the link.
    """
    class Meta:
        name = "inertial"
