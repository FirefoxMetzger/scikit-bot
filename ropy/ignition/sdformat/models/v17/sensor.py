from dataclasses import dataclass
from .sensor_type import SensorType


@dataclass
class Sensor(SensorType):
    """
    The sensor tag describes the type and properties of a sensor.
    """

    class Meta:
        name = "sensor"
