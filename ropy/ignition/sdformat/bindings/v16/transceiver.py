from dataclasses import dataclass
from .transceiver_type import TransceiverType


@dataclass
class Transceiver(TransceiverType):
    class Meta:
        name = "transceiver"
