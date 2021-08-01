from dataclasses import dataclass
from .model_state_type import ModelType


@dataclass
class Model(ModelType):
    class Meta:
        name = "model"
