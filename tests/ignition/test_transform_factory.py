import pytest
from pathlib import Path
import numpy as np

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


def test_v15_parsing(v15_sdf):
    try:
        frame = ign.sdformat.to_frame_graph(v15_sdf)
    except NotImplementedError:
        pytest.skip("Elements not implemented yet.")

    if isinstance(frame, list):
        assert len(frame) > 1
        for el in frame:
            assert isinstance(el, tf.Frame)
    else:
        assert isinstance(frame, tf.Frame)


def test_v15_refuted(v15_sdf_refuted):
    with pytest.raises(ign.sdformat.sdformat.ParseError):
        ign.sdformat.to_frame_graph(v15_sdf_refuted)


def test_panda():
    model_file = Path(__file__).parent / "sdf" / "robots" / "panda" / "model.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)


def test_nd_panda():
    model_file = Path(__file__).parent / "sdf" / "robots" / "panda" / "model.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string, shape=(5, 3))


def test_poses():
    model_file = Path(__file__).parent / "sdf" / "v18" / "pose_testing.sdf"
    sdf_string = model_file.read_text()

    world = ign.sdformat.to_frame_graph(sdf_string)
    frame_a = world.find_frame("world/A")
    frame_b = world.find_frame("world/B")
    frame_c = world.find_frame("world/C")
    frame_d = world.find_frame("world/D")

    # origin tests
    origin_a = frame_a.transform((0, 0, 0), world)
    origin_b = frame_b.transform((0, 0, 0), world)
    origin_c = frame_c.transform((0, 0, 0), world)
    origin_d = frame_d.transform((0, 0, 0), world)

    assert np.allclose(origin_a, (1, 2, 3))
    assert np.allclose(origin_b, (0, 0, 0))
    assert np.allclose(origin_c, (0, 0, 0))
    assert np.allclose(origin_d, (1, 2, 3))
    
    # test vector x
    vector_a = frame_a.transform((1, 0, 0), world)
    vector_b = frame_b.transform((1, 0, 0), world)
    vector_c = frame_c.transform((1, 0, 0), world)
    vector_d = frame_d.transform((1, 0, 0), world)

    assert np.allclose(vector_a, (2, 2, 3))
    assert np.allclose(vector_b, (0, 1, 0))
    assert np.allclose(vector_c, (0, 0, 1))
    assert np.allclose(vector_d, (1, 2, 4))
