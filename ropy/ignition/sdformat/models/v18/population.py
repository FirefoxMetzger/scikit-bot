from dataclasses import dataclass
from .population_type import PopulationType


@dataclass
class Population(PopulationType):
    """
    The population element defines how and where a set of models will be
    automatically populated in Gazebo.
    """
    class Meta:
        name = "population"
