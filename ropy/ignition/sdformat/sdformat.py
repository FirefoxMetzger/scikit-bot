from xml.etree import ElementTree
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.exceptions import ParserError as XSDataParserError
import io
from typing import Dict, Callable

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
    "1.8": SDFv18,
}

# recommended to reuse the same parser context
# see: https://xsdata.readthedocs.io/en/latest/xml.html
xml_ctx = XmlContext()


class ParseError(XSDataParserError):
    pass


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
    This function only checks the root tag and does not parse the entire string.

    """

    parser = ElementTree.iterparse(io.StringIO(sdf), events=("start",))

    _, root = next(parser)

    if root.tag != "sdf":
        raise ParseError("SDF root element not found.")

    if "version" in root.attrib:
        version = root.attrib["version"]
        if version not in _parser_roots.keys():
            raise ParseError(f"Invalid version: {version}")
        return root.attrib["version"]
    else:
        return default


def parse_sdf(
    sdf: str, sdf_version: str = None, custom_constructor: Dict[str, Callable] = None
):
    """Convert an XML string into a sdformat.models tree.

    Parameters
    ----------
    sdf : str
        The SDFormat XML to be parsed.
    version : str
        The SDFormat version to use while parsing. If None (default) it will
        automatically determine the version from the <sdf> element. If specified
        the given version will be used instead.
    custom_constructor : Dict[str, Callable]
        Tag-wise overwrite of the default class factory. If an SDF element's tag matches
        an element in overwrite.keys() then callable will replace the default class
        constructor.

    Returns
    -------
    SdfRoot : object
        An instance of ropy.ignition.models.vXX.SDF where XX corresponds to the
        version of the SDFormat XML.

    """

    def class_factory(clazz, params):
        tag_name: str = clazz.Meta.name
        if tag_name in custom_constructor:
            return custom_constructor[tag_name](**params)

        return clazz, params

    if sdf_version is None:
        version = get_sdf_version(sdf)
    else:
        version = sdf_version

    root_class = _parser_roots[version]

    if root_class is None:
        raise ParseError(f"Ropy currently doesnt support SDFormat v{version}")

    sdf_parser = XmlParser(ParserConfig(), context=xml_ctx)

    return sdf_parser.from_string(sdf, root_class)


def serialize_sdf(root_element) -> str:
    """Serialize a SDFormat object to an XML string.

    Parameters
    ----------
    root_element : object
        An instance of ropy.ignition.models.vXX.SDF. XX represents the SDFormat
        version and can be any version currently supported by ropy.

    Returns
    -------
    sdformat_string : str
        A string containing SDFormat XML representing the given input.

    """
    serializer = XmlSerializer(config=SerializerConfig())
    buffer = io.StringIO()

    serializer.write(buffer, root_element)

    return buffer.read()
