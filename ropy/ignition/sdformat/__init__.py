"""
SDFormat XML parsing and serialization

The API used here mimics the API used by the familiar `JSON parser <json>`_ or
`YAML parser <yaml>`_. The main difference is that this module returns an object
tree of dataclass objects, whilst JSON and YAML return dictionaries.

Another difference is version handling, as SDFormat doesnt't rely on SemVer, and
different SDF versions require different parsers. This is handled internally;
however, it does result in you getting the option to explicitly specify the
version to be used while parsing, which could become more relevant here than
compared to JSON or YAML.

Functions
---------

.. autosummary::
    :toctree:
    
    ropy.ignition.sdformat.get_version
    ropy.ignition.sdformat.loads
    ropy.ignition.sdformat.dumps

.. _yaml: https://pyyaml.org/wiki/PyYAMLDocumentation
.. _json: https://docs.python.org/3/library/json.html

"""

from .sdformat import loads, dumps, get_version

__all__ = ["get_version", "loads", "dumps"]
