from dataclasses import dataclass
from .material_type import MaterialType


@dataclass
class Material(MaterialType):
    """
    The material of the visual element.
    """
    class Meta:
        name = "material"
