from dataclasses import dataclass
from .imu_type import ImuType


@dataclass
class Imu(ImuType):
    """
    These elements are specific to the IMU sensor.
    """

    class Meta:
        name = "imu"
