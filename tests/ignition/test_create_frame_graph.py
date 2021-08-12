import pytest
import numpy as np

import skbot.ignition as ign


def test_light(valid_sdf_string):
    if ign.sdformat.get_version(valid_sdf_string) != "1.8":
        pytest.skip("Wrong Version")
    ign.create_frame_graph(valid_sdf_string)
