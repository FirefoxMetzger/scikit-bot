from dataclasses import dataclass
from .contact_type import ContactType


@dataclass
class Contact(ContactType):
    class Meta:
        name = "contact"
