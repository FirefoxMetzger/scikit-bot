from dataclasses import dataclass
from .forcetorque_type import ForceTorqueType


@dataclass
class ForceTorque(ForceTorqueType):
    """
    These elements are specific to the force torque sensor.
    """

    class Meta:
        name = "force_torque"
