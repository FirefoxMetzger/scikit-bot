from dataclasses import dataclass
import numpy as np
import pytest
from xsdata.exceptions import ParserError
from ropy.ignition.sdformat.models.v16.pose_type import PoseType

import ropy.ignition as ign


def test_valid_parsing(valid_sdf_string):
    """
    Test is successful if it doesn't produce an error. This isn't super amazing
    so it might be refactored once I have more sophisticated tests. Meanwhile it
    hits on quite a few edge cases of the SDFormat that need to be handled
    correctly.
    """
    ign.sdformat.loads(valid_sdf_string)


def test_invalid_parsing(invalid_sdf_string):
    with pytest.raises(ParserError):
        ign.sdformat.loads(invalid_sdf_string)


@pytest.mark.skip(reason="Currently disabled.")
def test_custom_constructor(valid_sdf_string):
    @dataclass
    class NewPose:
        value: str

        def __post_init__(self):
            try:
                self.value = tuple(float(x) for x in self.value.split(" "))
            except ValueError:
                pass

    if ign.sdformat.get_version(valid_sdf_string) != "1.6":
        return
    else:
        ign.sdformat.loads(
            valid_sdf_string,
            custom_constructor={PoseType: lambda **kwargs: NewPose(**kwargs)},
        )


def test_idempotence(valid_sdf_string):
    # serializing twice should be idempotent
    # the first serialization should normalize the XML
    # the second pass should make no changes

    # Note: the normalized XML doesn't use new-line
    # characters.

    parsed_sdf = ign.sdformat.loads(valid_sdf_string)
    normalized_sdf = ign.sdformat.dumps(parsed_sdf)

    parsed_sdf = ign.sdformat.loads(normalized_sdf)
    serialized_sdf = ign.sdformat.dumps(parsed_sdf)

    assert serialized_sdf == normalized_sdf


def test_light(light_sdf):
    frames, _ = ign.create_frame_graph(light_sdf)

    # check if all frames were created
    assert all(key in frames.keys() for key in ["/sdf", "/sdf/point_light"])

    # check if the origin is where it belongs
    result = frames["/sdf/point_light"].transform((0, 0, 0), "/sdf")
    expected = (0, 2, 2)
    assert np.allclose(result, expected)


def test_unsupported_sdf_version():
    sdf = ""

    with pytest.raises(ParserError):
        ign.sdformat.loads(sdf, version="1.0")
