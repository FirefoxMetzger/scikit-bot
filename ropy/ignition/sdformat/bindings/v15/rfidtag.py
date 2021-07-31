from dataclasses import dataclass
from .rfidtag_type import RfidType


@dataclass
class Rfid(RfidType):
    class Meta:
        name = "rfid"
