from dataclasses import dataclass, field
from typing import List
from .noise_type import NoiseType

__NAMESPACE__ = "sdformat/altimeter"


@dataclass
class AltimeterType:
    """
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
        }
    )
    vertical_velocity: List["AltimeterType.VerticalVelocity"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass
    class VerticalPosition:
        """
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
    class VerticalVelocity:
        """
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
