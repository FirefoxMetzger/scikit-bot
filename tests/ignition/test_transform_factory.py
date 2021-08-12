import pytest
import numpy as np

import skbot.ignition as ign


def test_sdformat_transform_factory(valid_sdf_string):
    if ign.sdformat.get_version(valid_sdf_string) != "1.8":
        pytest.skip("Wrong Version")
    ign.transform_graph_from_sdf(valid_sdf_string)
