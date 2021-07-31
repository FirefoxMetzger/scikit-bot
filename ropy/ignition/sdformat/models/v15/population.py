from dataclasses import dataclass
from .population_type import PopulationType


@dataclass
class Population(PopulationType):
    class Meta:
        name = "population"
