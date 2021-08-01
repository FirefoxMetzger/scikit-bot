from dataclasses import dataclass
from .lidar_type import LidarType


@dataclass
class Lidar(LidarType):
    class Meta:
        name = "lidar"
