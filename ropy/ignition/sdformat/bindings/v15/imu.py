from dataclasses import dataclass
from .imu_type import ImuType


@dataclass
class Imu(ImuType):
    class Meta:
        name = "imu"
