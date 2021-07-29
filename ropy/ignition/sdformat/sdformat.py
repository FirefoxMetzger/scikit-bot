from xml.etree import ElementTree
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser

from .models.v15 import Sdf as SDFv15
from .models.v16 import Sdf as SDFv16
from .models.v17 import Sdf as SDFv17
from .models.v18 import Sdf as SDFv18

# available SDF elements by version
_parser_roots = {
    "1.0": None,
    "1.2": None,
    "1.3": None,
    "1.4": None,
    "1.5": SDFv15,
    "1.6": SDFv16,
    "1.7": SDFv17,
    "1.8": SDFv18
}

# recommended to reuse the same parser instance
# see: https://xsdata.readthedocs.io/en/latest/xml.html
sdf_parser = XmlParser(XmlContext())


def get_sdf_version(sdf: str, default: str = "1.8"):
    """Returns the version of a SDF string.

    Parameters
    ----------
    sdf : str
        The SDFormat XML to be parsed.
    default : str
        If no version is specified, the default value is returned instead. It is
        equal to the latest SDF version supported by ropy.

    Notes
    -----
    This function only checks the root tag and does not parse the entire file.

    """

    root = ElementTree.fromstring(sdf)

    if root.tag != "sdf":
        raise ValueError("SDF root element not found.")

    if "version" in root.attrib:
        version = root.attrib["version"]
        if version not in _parser_roots.keys():
            raise ValueError(f"Invalid version: {version}")
        return root.attrib["version"]
    else:
        return default


def parse_sdf(sdf: str, sdf_version:str=None):
    """Returns the (version-aware)
    """

    if sdf_version is None:
        version = get_sdf_version(sdf)
    else:
        version = "1.8"

    root_class = _parser_roots[version]

    return sdf_parser.from_string(sdf, root_class)


def serialize_sdf(root_element) -> str:
    """
    """