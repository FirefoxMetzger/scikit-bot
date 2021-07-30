from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/battery"


@dataclass
class BatteryType:
    """
    Parameters
    ----------
    voltage: Initial voltage in volts.
    name: Unique name for the battery.
    """

    class Meta:
        name = "batteryType"

    voltage: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
