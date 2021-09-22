import pytest
from pathlib import Path
import numpy as np
from typing import Dict
from itertools import chain

import skbot.ignition as ign
import skbot.transform as tf
from skbot.ignition.sdformat.generic_sdf.base import ElementBase, Pose
from skbot.ignition.sdformat.generic_sdf.frame import Frame
from skbot.ignition.sdformat.generic_sdf.joint import Joint


def assert_recursive(tree, assert_fn):
    assert_fn(tree)

    for el in dir(tree):
        item = getattr(tree, el)
        if not isinstance(item, list):
            item = [item]

        for el2 in item:
            if isinstance(el2, ElementBase):
                assert_recursive(el2, assert_fn)


def test_v18_parsing(v18_worlds):
    try:
        frame = ign.sdformat.to_frame_graph(v18_worlds)
    except NotImplementedError:
        pytest.skip("Elements not implemented yet.")

    if isinstance(frame, list):
        assert len(frame) > 1
        for el in frame:
            assert isinstance(el, tf.Frame)
    else:
        assert isinstance(frame, tf.Frame)


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


def test_static_matches_dynamic():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    static_frames = world_sdf.declared_frames()
    static_graph = world_sdf.to_static_graph(static_frames)
    
    dynamic_frames = world_sdf.declared_frames()
    dynamic_graph = world_sdf.to_dynamic_graph(dynamic_frames)

    for key, value in dynamic_frames.items():
        assert key in static_frames
        assert value.name == static_frames[key].name

    frame_list = ign.sdformat.to_frame_graph(sdf_string, unwrap=False)

def test_declared_frames():
    def assert_matching_frames(frames):
        for name in frames.keys():
            if name.endswith("__model__"):
                implicit_name = name.rsplit("::", 1)[0]
                implicit_frame = frames[implicit_name]
                explicit_frame = frames[name]
                assert implicit_frame is explicit_frame

    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    for el in chain(generic_sdf.worlds):
        assert_matching_frames(el.declared_frames())
    if generic_sdf.model is not None:
        assert_matching_frames(generic_sdf.model.declared_frames())
    if generic_sdf.actor is not None:
        assert_matching_frames(generic_sdf.actor.declared_frames())
    if generic_sdf.light is not None:
        assert_matching_frames(generic_sdf.light.declared_frames())


def test_static_graph():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    static_frames = world_sdf.declared_frames()
    world_frame = world_sdf.to_static_graph(static_frames)

    # each frame should be reachable from the root frame
    for name, frame in static_frames.items():
        # will raise exception on mising chain
        tf_chain = world_frame.transform_chain(frame)


def test_dynamic_graph():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    static_frames = world_sdf.declared_frames()
    world_frame = world_sdf.to_static_graph(static_frames)

    all_frames = world_sdf.declared_frames()
    dynamic_world_frame = world_sdf.to_dynamic_graph(all_frames)

def test_unwrapping():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    frame_list = ign.sdformat.to_frame_graph(sdf_string, unwrap=False)

    assert isinstance(frame_list, list)
    for el in frame_list:
        assert isinstance(el, tf.Frame)


def test_pose_relative_to_leaking():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)

    def pose_has_relative_to(element):
        if isinstance(element, Pose):
            assert element.relative_to is not None
            assert element.relative_to != ""
    
    assert_recursive(generic_sdf, pose_has_relative_to)
        

def test_frame_attached_to_leaking():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)

    def pose_has_relative_to(element):
        if isinstance(element, Frame):
            assert element.attached_to is not None
            assert element.attached_to != ""
    
    assert_recursive(generic_sdf, pose_has_relative_to)


def test_joint_axis_expressed_in_leaking():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)

    def pose_has_relative_to(element):
        if isinstance(element, Joint.Axis.Xyz):
            assert element.expressed_in is not None
            assert element.expressed_in != ""
    
    assert_recursive(generic_sdf, pose_has_relative_to)


def test_panda():
    model_file = Path(__file__).parent / "sdf" / "robots" / "panda" / "model.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)


def test_nd_panda():
    model_file = Path(__file__).parent / "sdf" / "robots" / "panda" / "model.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string, shape=(5, 3))


def test_must_be_base_link():
    model_file = Path(__file__).parent / "sdf" / "v18" / "pose_testing.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    frames = world_sdf.declared_frames()
    world_frame = world_sdf.to_dynamic_graph(frames)

    for name in ["A", "B", "C", "D"]:
        chain = world_frame.transform_chain(name)
        assert len(chain) == 1

        chain = world_frame.find_frame(f"world/{name}").transform_chain(world_frame)
        assert len(chain) == 1

def test_poses():
    model_file = Path(__file__).parent / "sdf" / "v18" / "pose_testing.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    static_frames = world_sdf.declared_frames()
    static_graph = world_sdf.to_static_graph(static_frames)

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
    assert np.allclose(vector_c, (0, 1, 0))
    assert np.allclose(vector_d, (1, 3, 3))

def test_poses_relative_to():
    model_file = Path(__file__).parent / "sdf" / "v18" / "pose_relative_to.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    static_frames = world_sdf.declared_frames()
    static_graph = world_sdf.to_static_graph(static_frames)

    cam_link = static_frames["camera::link"]
    box_link = static_frames["box::box_link"]

    # origin tests
    origin_cam = cam_link.transform((0, 0, 0), static_frames["world"])
    origin_box = box_link.transform((0, 0, 0), static_frames["world"])

    assert np.allclose(origin_cam, (2.0003185305832973, 0.19999974634550793, 1.75))
    assert np.allclose(origin_box, (0.8305268741307381, -0.237974865830905, 1.0399999999999998))

    # test vector x
    vector_cam = cam_link.transform((1, 0, 0), static_frames["world"])
    vector_box = box_link.transform((1, 0, 0), static_frames["world"])

    assert np.allclose(vector_cam, (1.0400594540571846, 0.2015291077039671, 1.4708939860858379))
    
    # I can not get ground truth for this test case :(
    # assert np.allclose(vector_box, (0, 1, 0))

def test_double_pendulum():
    model_file = (
        Path(__file__).parent / "sdf" / "robots" / "double_pendulum" / "model.sdf"
    )
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)


def test_perspective_transform_straight():
    model_file = (
        Path(__file__).parent / "sdf" / "v18" / "perspective_transform_straight.sdf"
    )
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)
    px_space = root_frame.find_frame(".../pixel-space")
    box = root_frame.find_frame(".../box_visual")
    center = np.array([0, 0, 0])
    corners = np.array(
        [
            [-0.025, 0.025, 0.025],
            [-0.025, 0.025, -0.025],
            [-0.025, -0.025, 0.025],
            [-0.025, -0.025, -0.025],
        ]
    )

    center_px = box.transform(center, px_space)
    expected_center = np.array([500, 500])
    assert np.allclose(center_px, expected_center)

    corner_px = box.transform(corners, px_space)
    expected_corners = np.array(
        [
            [159.17765576, 159.17765576],
            [840.82234424, 159.17765576],
            [159.17765576, 840.82234424],
            [840.82234424, 840.82234424],
        ]
    )
    assert np.allclose(corner_px, expected_corners)


def test_perspective_transform_offset():
    model_file = (
        Path(__file__).parent / "sdf" / "v18" / "perspective_transform_offset.sdf"
    )
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)
    px_space = root_frame.find_frame(".../pixel-space")
    box = root_frame.find_frame(".../box_visual")
    center = np.array([0, 0, 0])
    corners = np.array(
        [
            [-0.025, 0.025, 0.025],
            [-0.025, 0.025, -0.025],
            [-0.025, -0.025, 0.025],
            [-0.025, -0.025, -0.025],
        ]
    )

    center_px = box.transform(center, px_space)
    expected_center = np.array([159.17765576, 159.17765576])
    assert np.allclose(center_px, expected_center)

    corner_px = box.transform(corners, px_space)
    expected_corners = np.array(
        [
            [94.259114, 256.5554684],
            [256.5554684, 256.5554684],
            [94.259114, 94.259114],
            [256.5554684, 94.259114],
        ]
    )
    assert np.allclose(corner_px, expected_corners)


def test_perspective_transform_rotations():
    model_file = Path(__file__).parent / "sdf" / "v18" / "perspective_transform.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)
    px_space = root_frame.find_frame(".../pixel-space")
    box = root_frame.find_frame(".../box_visual")
    center = np.array([0, 0, 0])
    corners = np.array(
        [
            [0.025, 0.025, 0.025],
            [0.025, -0.025, 0.025],
            [0.025, 0.025, -0.025],
            [0.025, -0.025, -0.025],
            [-0.025, 0.025, 0.025],
            [-0.025, 0.025, -0.025],
            [-0.025, -0.025, 0.025],
            [-0.025, -0.025, -0.025],
        ]
    )

    center_px = box.transform(center, px_space)
    expected_center = np.array([696.11915148, 500.0])
    assert np.allclose(center_px, expected_center)

    corner_px = box.transform(corners, px_space)
    expected_corners = np.array(
        [
            [667.51733424, 483.00101919],
            [843.08517093, 337.00889243],
            [745.4267735, 707.52604657],
            [903.5973054, 555.82971401],
            [483.00856364, 442.65467015],
            [564.65438813, 645.79960364],
            [652.15261944, 314.95354669],
            [718.30507077, 513.1858061],
        ]
    )
    print(corner_px)
    assert np.allclose(corner_px, expected_corners)


def test_link_offset():
    model_file = Path(__file__).parent / "sdf" / "v18" / "link_offset.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)
    cam_base = root_frame.find_frame(".../camera::__model__")
    cam_link = cam_base.find_frame("camera::__model__/link")
    cam_space = cam_base.find_frame(".../camera/camera-space")
    
    actual = cam_link.transform((0,0,0), root_frame)
    expected = (0.8003185305832974, 0.19999974634550793, 1.35)

    # the accuraccy here is quite low. TODO: investigate which rotation is
    # more accurate
    assert np.allclose(actual, expected, atol=1e-2)



def test_four_goals():
    model_file = Path(__file__).parent / "sdf" / "v18" / "four_goals.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)
    cam_base = root_frame.find_frame(".../main_camera::__model__")
    px_space = cam_base.find_frame(".../pixel-space")
    cam_space = cam_base.find_frame(".../camera-space")

    box_base = root_frame.find_frame(".../box_copy_0::__model__")
    box = root_frame.find_frame(".../box_visual")
    vertices = np.array(
        [
            [0.025, 0.025, 0.025],  # 0
            [0.025, -0.025, 0.025],
            [0.025, 0.025, -0.025],
            [0.025, -0.025, -0.025],
            [-0.025, 0.025, 0.025],
            [-0.025, 0.025, -0.025],  # 5
            [-0.025, -0.025, 0.025],
            [-0.025, -0.025, -0.025],
        ]
    )

    edges = [
        (0, 1),
        (0, 2),
        (0, 4),
        (1, 3),
        (1, 6),
        (2, 3),
        (2, 5),
        (3, 7),
        (4, 5),
        (4, 6),
        (5, 7),
        (6, 7),
    ]

    center = np.array([0, 0, 0])

    from matplotlib.patches import Circle
    import matplotlib.pyplot as plt
    import imageio as iio

    img = iio.imread("front_view.png")
    _, ax = plt.subplots(1)
    ax.imshow(img)
    corner_px = box.transform(vertices, px_space)
    distance = list()
    for idx_a, idx_b in edges:
        x = np.linspace(corner_px[idx_a, 1], corner_px[idx_b, 1], 100)
        y = np.linspace(corner_px[idx_a, 0], corner_px[idx_b, 0], 100)
        ax.plot(x, y, "blue")
        distance.append(np.linalg.norm(y - x))

    # ax.scatter(corner_px[:, 1], corner_px[:, 0], 10)
    ax.add_patch(Circle(box.transform(center, px_space)[::-1], radius=3, color="red"))

    # centered_corner_px = cam_space.transform(vertices+np.array([0.5, 0, 0]), px_space)
    # ax.scatter(centered_corner_px[:, 1], centered_corner_px[:, 0], 10)
    plt.show()

    print("")
