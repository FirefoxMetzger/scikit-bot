import pytest
import numpy as np
from pathlib import Path

import skbot.ignition as ign


def test_sdformat_transform_factory(valid_sdf_string):
    if ign.sdformat.get_version(valid_sdf_string) != "1.8":
        pytest.skip("Wrong Version")
    ign.transform_graph_from_sdf(valid_sdf_string)


def test_panda():
    model_file = Path(__file__).parent / "sdf" / "robots" / "panda" / "model.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.transform_graph_from_sdf(sdf_string)
