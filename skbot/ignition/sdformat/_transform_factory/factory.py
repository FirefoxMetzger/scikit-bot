from typing import Callable, Dict
import importlib

from .. import sdformat
from .graph import Graph


# available SDF elements by version
_converter_roots = {
    "1.0": None,
    "1.2": None,
    "1.3": None,
    "1.4": None,
    "1.5": None,
    "1.6": None,
    "1.7": None,
    "1.8": "..v18",
}


class GraphFactory:
    """A factory that turns SDF of different versions into generic graphs
    that can then be assembled into transform graphs"""
    converters: Dict[str, Callable] = dict()

    def __call__(self, sdf:str, *, unwrap=True) -> Graph:
        version = sdformat.get_version(sdf)
        if version not in self.converters.keys():
            # lazy loading of SDF bindings
            converter_module = _converter_roots[version]
            if converter_module is None:
                raise NotImplementedError(f"SDFormat v{version} is not supported yet.")
            mod = importlib.import_module(converter_module, __name__)
            self.converters[version] = mod.converter

        return self.converters[version](sdf, unwrap=unwrap)

# a singleton
graph_factory = GraphFactory()