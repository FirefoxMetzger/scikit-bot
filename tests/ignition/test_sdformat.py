from dataclasses import dataclass
import numpy as np
import pytest
from xsdata.exceptions import ParserError
from pathlib import Path

from skbot.ignition.sdformat.bindings.v16.model import Model
import skbot.ignition as ign


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


def test_invalid_parsing_xml_etree(invalid_sdf_string):
    with pytest.raises(ParserError):
        ign.sdformat.loads(invalid_sdf_string, handler="XmlEventHandler")


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
            custom_constructor={Model.Pose: lambda **kwargs: NewPose(**kwargs)},
        )


def test_idempotence(valid_sdf_string):
    # serializing twice should be idempotent
    # the first serialization should normalize the XML
    # the second pass should make no changes

    parsed_sdf = ign.sdformat.loads(valid_sdf_string)
    normalized_sdf = ign.sdformat.dumps(parsed_sdf)

    parsed_sdf = ign.sdformat.loads(normalized_sdf)
    serialized_sdf = ign.sdformat.dumps(parsed_sdf)

    assert serialized_sdf == normalized_sdf


def test_force_version():
    sdf_file = Path(__file__).parent / "sdf" / "sdformat" / "empty.sdf"

    ign.sdformat.loads(sdf_file.read_text(), version="1.8")
