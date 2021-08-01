from dataclasses import dataclass, field
from typing import List
from .noise_type import NoiseType

__NAMESPACE__ = "sdformat/air_pressure"


@dataclass
class AirPressureType:
    """
    These elements are specific to an air pressure sensor.

    Parameters
    ----------
    reference_altitude: The initial altitude in meters. This value can
        be used by a sensor implementation to augment the altitude of
        the sensor. For example, if you are using simulation instead of
        creating a 1000 m mountain model on which to place your sensor,
        you could instead set this value to 1000 and place your model on
        a ground plane with a Z height of zero.
    pressure: Noise parameters for the pressure data.
    """

    class Meta:
        name = "air_pressureType"

    reference_altitude: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pressure: List["AirPressureType.Pressure"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass
    class Pressure:
        """
        Noise parameters for the pressure data.

        Parameters
        ----------
        noise: The properties of a sensor noise model.
        """

        noise: List[NoiseType] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
