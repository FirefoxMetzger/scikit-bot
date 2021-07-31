from dataclasses import dataclass, field
from typing import List
from .noise_type import NoiseType

__NAMESPACE__ = "sdformat/gps"


@dataclass
class GpsType:
    """
    These elements are specific to the GPS sensor.

    Parameters
    ----------
    position_sensing: Parameters related to GPS position measurement.
    velocity_sensing: Parameters related to GPS position measurement.
    """

    class Meta:
        name = "gpsType"

    position_sensing: List["GpsType.PositionSensing"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    velocity_sensing: List["GpsType.VelocitySensing"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass
    class PositionSensing:
        """
        Parameters related to GPS position measurement.

        Parameters
        ----------
        horizontal: Noise parameters for horizontal position
            measurement, in units of meters.
        vertical: Noise parameters for vertical position measurement, in
            units of meters.
        """

        horizontal: List["GpsType.PositionSensing.Horizontal"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        vertical: List["GpsType.PositionSensing.Vertical"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Horizontal:
            """
            Noise parameters for horizontal position measurement, in units of
            meters.

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

        @dataclass
        class Vertical:
            """
            Noise parameters for vertical position measurement, in units of
            meters.

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

    @dataclass
    class VelocitySensing:
        """
        Parameters related to GPS position measurement.

        Parameters
        ----------
        horizontal: Noise parameters for horizontal velocity
            measurement, in units of meters/second.
        vertical: Noise parameters for vertical velocity measurement, in
            units of meters/second.
        """

        horizontal: List["GpsType.VelocitySensing.Horizontal"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        vertical: List["GpsType.VelocitySensing.Vertical"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Horizontal:
            """
            Noise parameters for horizontal velocity measurement, in units of
            meters/second.

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

        @dataclass
        class Vertical:
            """
            Noise parameters for vertical velocity measurement, in units of
            meters/second.

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
