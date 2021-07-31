from dataclasses import dataclass
from .plugin_type import PluginType


@dataclass
class Plugin(PluginType):
    class Meta:
        name = "plugin"
