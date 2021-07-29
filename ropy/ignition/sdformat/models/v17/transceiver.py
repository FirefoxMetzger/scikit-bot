from dataclasses import dataclass
from .transceiver_type import TransceiverType


@dataclass
class Transceiver(TransceiverType):
    """
    These elements are specific to a wireless transceiver.
    """
    class Meta:
        name = "transceiver"
