from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/plugin"


@dataclass
class PluginType:
    """
    Parameters
    ----------
    any_element: This is a special element that should not be specified
        in an SDFormat file. It automatically copies child elements into
        the SDFormat element so that a plugin can access the data.
    name: A unique name for the plugin, scoped to its parent.
    filename: Name of the shared library to load. If the filename is not
        a full path name, the file will be searched for in the
        configuration paths.
    """
    class Meta:
        name = "pluginType"

    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    filename: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
