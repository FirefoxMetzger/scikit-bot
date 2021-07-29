from pathlib import Path
import numpy as np
import pytest
from xsdata.exceptions import ParserError
from xml.etree.ElementTree import ParseError as ETreeParseError

import ropy.ignition as ign


def test_valid_parsing(valid_sdf_string):
    """
    Test is successful if it doesn't produce an error. This isn't super amazing
    so it might be refactored once I have more sophisticated tests. Meanwhile it
    hits on quite a few edge cases of the SDFormat that need to be handled
    correctly.
    """
    ign.parse_sdf(valid_sdf_string)


def test_invalid_parsing(invalid_sdf_string):
    with pytest.raises(ParserError):
        ign.parse_sdf(invalid_sdf_string)


def test_light(light_sdf):
    frames, links = ign.create_frame_graph(light_sdf)

    # check if all frames were created
    assert all(key in frames.keys() for key in ["/sdf", "/sdf/point_light"])

    # check if the origin is where it belongs
    result = frames["/sdf/point_light"].transform((0, 0, 0), "/sdf")
    expected = (0, 2, 2)
    assert np.allclose(result, expected)
