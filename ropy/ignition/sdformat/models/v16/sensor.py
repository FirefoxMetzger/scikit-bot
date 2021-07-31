from dataclasses import dataclass
from .sensor_type import SensorType


@dataclass
class Sensor(SensorType):
    class Meta:
        name = "sensor"
