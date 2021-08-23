import pytest
from pathlib import Path

import skbot.ignition as ign
import skbot.transform as tf


def test_v18_parsing(v18_sdf):
    try:
        frame = ign.sdformat.to_frame_graph(v18_sdf)
    except NotImplementedError:
        pytest.skip("Elements not implemented yet.")
    
    if isinstance(frame, list):
        assert len(frame) > 1
        for el in frame:
            assert isinstance(el, tf.Frame)
    else:
        assert isinstance(frame, tf.Frame)


def test_v18_parsing_wrapped(v18_sdf):
    try:
        frame_list = ign.sdformat.to_frame_graph(v18_sdf, unwrap=False)
    except NotImplementedError:
        pytest.skip("Elements not implemented yet.")

    for el in frame_list:
        assert isinstance(el, tf.Frame)


def test_v18_refuted(v18_sdf_refuted):
    with pytest.raises(ign.sdformat.sdformat.ParseError):
        ign.sdformat.to_frame_graph(v18_sdf_refuted)


def test_v17_parsing(v17_sdf):
    try:
        frame = ign.sdformat.to_frame_graph(v17_sdf)
    except NotImplementedError:
        pytest.skip("Elements not implemented yet.")
    
    if isinstance(frame, list):
        assert len(frame) > 1
        for el in frame:
            assert isinstance(el, tf.Frame)
    else:
        assert isinstance(frame, tf.Frame)

def test_v17_refuted(v17_sdf_refuted):
    with pytest.raises(ign.sdformat.sdformat.ParseError):
        ign.sdformat.to_frame_graph(v17_sdf_refuted)


def test_panda():
    model_file = Path(__file__).parent / "sdf" / "robots" / "panda" / "model.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)

def test_nd_panda():
    model_file = Path(__file__).parent / "sdf" / "robots" / "panda" / "model.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string, shape=(5, 3))
