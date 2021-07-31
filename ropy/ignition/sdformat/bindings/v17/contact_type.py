from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/contact"


@dataclass
class ContactType:
    """
    These elements are specific to the contact sensor.

    Parameters
    ----------
    collision: name of the collision element within a link that acts as
        the contact sensor.
    topic: Topic on which contact data is published.
    """
    class Meta:
        name = "contactType"

    collision: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    topic: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
