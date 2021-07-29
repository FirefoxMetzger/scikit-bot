from dataclasses import dataclass
from .link_state_type import LinkType


@dataclass
class Link(LinkType):
    """
    Link state.
    """
    class Meta:
        name = "link"
