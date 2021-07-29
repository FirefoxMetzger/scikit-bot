from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from models.v18 import Sdf
from pathlib import Path

import pytest

@pytest.mark.parametrize("file", [
    "~/ropy/ropy/ignition/toy/panda_world.sdf",
    "~/ropy/ropy/ignition/toy/world_with_state.sdf",
    *[str(x) for x in Path("~/workspace/src/sdformat/test/sdf/").expanduser().iterdir()]
])
def test_parse(file:str):
    """Consired success if parsing doesn't crash"""

    file = Path(file).expanduser()

    if not file.suffix in [".sdf", ".world"]:
        pytest.skip("Not a SDF file.")

    parser = XmlParser(context=XmlContext())
    foo = parser.parse(str(file), Sdf)