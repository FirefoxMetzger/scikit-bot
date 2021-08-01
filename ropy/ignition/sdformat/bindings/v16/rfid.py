from dataclasses import dataclass
from .rfid_type import RfidtagType


@dataclass
class Rfidtag(RfidtagType):
    class Meta:
        name = "rfidtag"
