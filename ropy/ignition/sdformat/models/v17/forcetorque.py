from dataclasses import dataclass
from .forcetorque_type import ForceTorqueType


@dataclass
class ForceTorque(ForceTorqueType):
    class Meta:
        name = "force_torque"
