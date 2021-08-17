import pytest
from pathlib import Path

import skbot.ignition as ign
import skbot.transform as tf


def test_v18_parsing(v18_sdf):
    frame = ign.transform_graph_from_sdf(v18_sdf)
    assert isinstance(frame, tf.Frame)


def test_v18_parsing_wrapped(v18_sdf):
    frame_list = ign.transform_graph_from_sdf(v18_sdf, unwrap=False)

    assert isinstance(frame_list, list)
    for frame in frame_list:
        assert isinstance(frame, tf.Frame)


def test_v18_refuted(v18_sdf_refuted):
    with pytest.raises(ign.sdformat.sdformat.ParseError):
        ign.transform_graph_from_sdf(v18_sdf_refuted)


def test_panda():
    model_file = Path(__file__).parent / "sdf" / "robots" / "panda" / "model.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.transform_graph_from_sdf(sdf_string)
