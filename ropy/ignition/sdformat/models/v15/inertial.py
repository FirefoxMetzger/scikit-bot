from dataclasses import dataclass
from .inertial_type import InertialType


@dataclass
class Inertial(InertialType):
    class Meta:
        name = "inertial"
