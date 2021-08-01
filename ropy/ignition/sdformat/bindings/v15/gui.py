from dataclasses import dataclass
from .gui_type import GuiType


@dataclass
class Gui(GuiType):
    class Meta:
        name = "gui"
