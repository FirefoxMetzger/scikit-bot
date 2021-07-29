from dataclasses import dataclass
from .plugin_type import PluginType


@dataclass
class Plugin(PluginType):
    """A plugin is a dynamically loaded chunk of code.

    It can exist as a child of world, model, and sensor.
    """
    class Meta:
        name = "plugin"
