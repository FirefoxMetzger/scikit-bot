from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/atmosphere"


@dataclass
class AtmosphereType:
    """
    The atmosphere tag specifies the type and properties of the atmosphere
    model.

    Parameters
    ----------
    temperature: Temperature at sea level in kelvins.
    pressure: Pressure at sea level in pascals.
    temperature_gradient: Temperature gradient with respect to
        increasing altitude at sea level in units of K/m.
    type: The type of the atmosphere engine. Current options are
        adiabatic.  Defaults to adiabatic if left unspecified.
    """
    class Meta:
        name = "atmosphereType"

    temperature: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    pressure: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    temperature_gradient: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
