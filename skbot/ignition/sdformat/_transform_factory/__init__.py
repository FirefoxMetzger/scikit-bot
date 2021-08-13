from typing import Dict, Tuple, Union, List

from graph import Graph
from .... import transform as tf

LinkDict = Dict[str, tf.Link]
ConverterReturn = Tuple[Union[Graph, List[Graph]], LinkDict]