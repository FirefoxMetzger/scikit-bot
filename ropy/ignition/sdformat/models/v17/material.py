from dataclasses import dataclass
from .material_type import MaterialType


@dataclass
class Material(MaterialType):
    class Meta:
        name = "material"
