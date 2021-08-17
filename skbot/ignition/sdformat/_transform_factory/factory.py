from typing import Callable, Dict, Union, List, Any
import importlib
from urllib.parse import urlparse

from .. import sdformat
from .scopes import ModelScope, Scope
from ...fuel import get_fuel_model


# available SDF elements by version
_converter_roots = {
    "1.0": None,
    "1.2": None,
    "1.3": None,
    "1.4": None,
    "1.5": None,
    "1.6": None,
    "1.7": "..v17",
    "1.8": "..v18",
}


class FactoryBase:
    def __init__(self, *, unwrap=True, root_uri: str = None):
        self.root_uri: str = root_uri
        self.unwrap: bool = unwrap

    def __call__(self, sdf: str) -> Union[Scope, List[Scope]]:
        raise NotImplementedError()

    def _resolve_include(self, uri: str) -> ModelScope:
        # there is only one fuel server
        fuel_server = "fuel.ignitionrobotics.org"
        uri_parts = urlparse(uri)

        if uri_parts.scheme == "https" and uri_parts.netloc == fuel_server:
            root_uri = uri
            rel_path = "model.sdf"
        elif uri_parts.scheme == "model":
            raise NotImplementedError("Unsure how to resolve model://.")
        elif uri_parts.scheme == "":
            rel_path = uri
        else:
            raise sdformat.ParseError(f"Unknown URI: {uri}")

        sdf = get_fuel_model(root_uri, file_path=rel_path)
        return transform_factory(sdf, root_uri=root_uri)


class TransformFactory:
    """A factory that turns SDF of different versions into generic graphs
    that can then be assembled into transform graphs"""

    converters: Dict[str, Callable[[Any], Union[Scope, List[Scope]]]] = dict()

    def __call__(self, sdf: str, *, unwrap=True, root_uri: str = None) -> Scope:
        version = sdformat.get_version(sdf)
        if version not in self.converters.keys():
            # lazy loading of SDF bindings
            converter_module = _converter_roots[version]
            if converter_module is None:
                raise NotImplementedError(f"SDFormat v{version} is not supported yet.")
            mod = importlib.import_module(converter_module, __name__)
            self.converters[version] = mod.Converter

        return self.converters[version](root_uri=root_uri, unwrap=unwrap)(sdf)


# a singleton
transform_factory = TransformFactory()
