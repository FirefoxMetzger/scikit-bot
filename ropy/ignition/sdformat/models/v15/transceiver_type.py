from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/transceiver"


@dataclass
class TransceiverType:
    """
    These elements are specific to a wireless transceiver.

    Parameters
    ----------
    essid: Service set identifier (network name)
    frequency: Specifies the frequency of transmission in MHz
    min_frequency: Only a frequency range is filtered. Here we set the
        lower bound (MHz).
    max_frequency: Only a frequency range is filtered. Here we set the
        upper bound (MHz).
    gain: Specifies the antenna gain in dBi
    power: Specifies the transmission power in dBm
    sensitivity: Mininum received signal power in dBm
    """

    class Meta:
        name = "transceiverType"

    essid: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    frequency: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    min_frequency: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    max_frequency: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gain: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    power: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    sensitivity: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
