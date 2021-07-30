from dataclasses import dataclass
from .lidar_type import LidarType


@dataclass
class Lidar(LidarType):
    """
    These elements are specific to the lidar sensor.
    """

    class Meta:
        name = "lidar"
