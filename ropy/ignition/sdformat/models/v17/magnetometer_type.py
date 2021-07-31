from dataclasses import dataclass, field
from typing import List
from .noise_type import NoiseType

__NAMESPACE__ = "sdformat/magnetometer"


@dataclass
class MagnetometerType:
    """
    These elements are specific to a Magnetometer sensor.

    Parameters
    ----------
    x: Parameters related to the body-frame X axis of the magnetometer
    y: Parameters related to the body-frame Y axis of the magnetometer
    z: Parameters related to the body-frame Z axis of the magnetometer
    """
    class Meta:
        name = "magnetometerType"

    x: List["MagnetometerType.X"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    y: List["MagnetometerType.Y"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    z: List["MagnetometerType.Z"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass
    class X:
        """
        Parameters related to the body-frame X axis of the magnetometer.

        Parameters
        ----------
        noise: The properties of a sensor noise model.
        """
        noise: List[NoiseType] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Y:
        """
        Parameters related to the body-frame Y axis of the magnetometer.

        Parameters
        ----------
        noise: The properties of a sensor noise model.
        """
        noise: List[NoiseType] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Z:
        """
        Parameters related to the body-frame Z axis of the magnetometer.

        Parameters
        ----------
        noise: The properties of a sensor noise model.
        """
        noise: List[NoiseType] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            }
        )
