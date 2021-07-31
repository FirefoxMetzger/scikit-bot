from dataclasses import dataclass, field
from typing import List
from .noise_type import NoiseType

__NAMESPACE__ = "sdformat/altimeter"


@dataclass
class AltimeterType:
    """
    These elements are specific to an altimeter sensor.

    Parameters
    ----------
    vertical_position: Noise parameters for vertical position
    vertical_velocity: Noise parameters for vertical velocity
    """

    class Meta:
        name = "altimeterType"

    vertical_position: List["AltimeterType.VerticalPosition"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    vertical_velocity: List["AltimeterType.VerticalVelocity"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass
    class VerticalPosition:
        """
        Noise parameters for vertical position.

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
    class VerticalVelocity:
        """
        Noise parameters for vertical velocity.

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
