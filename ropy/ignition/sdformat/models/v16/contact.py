from dataclasses import dataclass
from .contact_type import ContactType


@dataclass
class Contact(ContactType):
    """
    These elements are specific to the contact sensor.
    """
    class Meta:
        name = "contact"
