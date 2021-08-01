from dataclasses import dataclass
from .link_state_type import LinkType


@dataclass
class Link(LinkType):
    class Meta:
        name = "link"
