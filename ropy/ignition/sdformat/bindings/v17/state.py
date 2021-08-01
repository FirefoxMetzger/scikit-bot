from dataclasses import dataclass
from .state_type import StateType


@dataclass
class State(StateType):
    class Meta:
        name = "state"
