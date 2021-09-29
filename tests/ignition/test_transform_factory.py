import pytest
from pathlib import Path
import numpy as np
from itertools import chain

import skbot.ignition as ign
import skbot.transform as tf
from skbot.ignition.sdformat.generic_sdf.base import ElementBase, Pose
from skbot.ignition.sdformat.generic_sdf.frame import Frame
from skbot.ignition.sdformat.generic_sdf.joint import Joint


pytestmark = pytest.mark.filterwarnings(
    "ignore::UserWarning", "ignore::DeprecationWarning"
)


def assert_recursive(tree, assert_fn):
    assert_fn(tree)

    for el in dir(tree):
        item = getattr(tree, el)

        if not isinstance(item, list):
            item = [item]

        for el2 in item:
            if isinstance(el2, ElementBase):
                assert_recursive(el2, assert_fn)


def test_static_matches_dynamic():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    static_frames = world_sdf.declared_frames()
    static_root = world_sdf.to_static_graph(static_frames)

    dynamic_frames = world_sdf.declared_frames()
    dynamic_root = world_sdf.to_dynamic_graph(dynamic_frames, apply_state=False)

    # assert that frames are similar
    for key, value in dynamic_frames.items():
        assert key in static_frames
        assert value.name == static_frames[key].name
        assert value.ndim == static_frames[key].ndim

    # assert that transformations yield similar result
    for name in dynamic_frames:
        dynamic_frame = dynamic_frames[name]
        static_frame = static_frames[name]

        null = np.zeros(dynamic_frame.ndim)
        try:
            world_coords = dynamic_frame.transform(null, dynamic_root)
        except RuntimeError:
            continue
        else:
            expected = static_frame.transform(null, static_root)
            assert np.allclose(world_coords, expected)


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


def test_static_graph(verifiable_sdf_string):
    generic_sdf = ign.sdformat.loads_generic(verifiable_sdf_string)
    static_frame_dict = generic_sdf.declared_frames()
    root_dict = generic_sdf.to_static_graph(static_frame_dict)

    for key in ["worlds", "models"]:
        frames = static_frame_dict[key]
        roots = root_dict[key]
        for static_frames, root in zip(frames, roots):
            # each frame should be reachable from the root frame
            for name, frame in static_frames.items():
                try:
                    tf_chain = root.transform_chain(frame)
                except RuntimeError:
                    raise AssertionError(
                        "A Frame in the static graph is unreachable."
                    ) from None


def test_dynamic_graph(verifiable_sdf_string):
    generic_sdf = ign.sdformat.loads_generic(verifiable_sdf_string)

    all_frames = generic_sdf.declared_frames()
    dynamic_world_frame = generic_sdf.to_dynamic_graph(all_frames)


def test_unwrapping():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    frame = ign.sdformat.to_frame_graph(sdf_string)

    assert isinstance(frame, tf.Frame)


def test_wrapped():
    model_file = Path(__file__).parent / "sdf" / "v18" / "world_with_state.sdf"
    sdf_string = model_file.read_text()

    frame_list = ign.sdformat.to_frame_graph(sdf_string, unwrap=False)

    assert isinstance(frame_list, list)
    for el in frame_list:
        assert isinstance(el, tf.Frame)


def test_pose_relative_to_leaking(verifiable_sdf_string):
    generic_sdf = ign.sdformat.loads_generic(verifiable_sdf_string)

    def pose_has_relative_to(element):
        if isinstance(element, Pose):
            assert element.relative_to is not None
            assert element.relative_to != ""

    assert_recursive(generic_sdf, pose_has_relative_to)


def test_frame_attached_to_leaking(verifiable_sdf_string):
    generic_sdf = ign.sdformat.loads_generic(verifiable_sdf_string)

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

    ## todo: assert that constructed shape is (5, 3)


def test_double_pendulum():
    model_file = (
        Path(__file__).parent / "sdf" / "robots" / "double_pendulum" / "model.sdf"
    )
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)


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


def test_poses_dynamic():
    model_file = Path(__file__).parent / "sdf" / "v18" / "pose_testing.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    frames = world_sdf.declared_frames()
    root = world_sdf.to_dynamic_graph(frames)

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

    frames = world_sdf.declared_frames()
    root = world_sdf.to_static_graph(frames)

    cam_link = frames["camera::link"]
    box_link = frames["box::box_link"]

    # origin tests
    origin_cam = cam_link.transform((0, 0, 0), frames["world"])
    origin_box = box_link.transform((0, 0, 0), frames["world"])

    assert np.allclose(origin_cam, (2.0003185305832973, 0.19999974634550793, 1.75))
    assert np.allclose(
        origin_box, (0.8305268741307381, -0.237974865830905, 1.0399999999999998)
    )

    # test vector x
    vector_cam = cam_link.transform((1, 0, 0), frames["world"])
    vector_box = box_link.transform((1, 0, 0), frames["world"])

    assert np.allclose(
        vector_cam, (1.0400594540571846, 0.2015291077039671, 1.4708939860858379)
    )

    # I can not get ground truth for this test case :(
    # assert np.allclose(vector_box, (0, 1, 0))


def test_poses_relative_to_dynamic():
    model_file = Path(__file__).parent / "sdf" / "v18" / "pose_relative_to.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    frames = world_sdf.declared_frames()
    root = world_sdf.to_static_graph(frames)

    cam_link = frames["camera::link"]
    box_link = frames["box::box_link"]

    # origin tests
    origin_cam = cam_link.transform((0, 0, 0), frames["world"])
    origin_box = box_link.transform((0, 0, 0), frames["world"])

    assert np.allclose(origin_cam, (2.0003185305832973, 0.19999974634550793, 1.75))
    assert np.allclose(
        origin_box, (0.8305268741307381, -0.237974865830905, 1.0399999999999998)
    )

    # test vector x
    vector_cam = cam_link.transform((1, 0, 0), frames["world"])
    vector_box = box_link.transform((1, 0, 0), frames["world"])

    assert np.allclose(
        vector_cam, (1.0400594540571846, 0.2015291077039671, 1.4708939860858379)
    )

    # I can not get ground truth for this test case :(
    # assert np.allclose(vector_box, (0, 1, 0))


def test_perspective_transform_straight():
    model_file = (
        Path(__file__).parent / "sdf" / "v18" / "perspective_transform_straight.sdf"
    )
    sdf_string = model_file.read_text()

    root_frame = ign.sdformat.to_frame_graph(sdf_string)
    px_space = root_frame.find_frame(".../pixel_space")
    box = root_frame.find_frame(".../box_link")
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
    px_space = root_frame.find_frame(".../pixel_space")
    box = root_frame.find_frame(".../box_link")
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
    px_space = root_frame.find_frame(".../pixel_space")
    box = root_frame.find_frame(".../box_link")
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

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    frames = world_sdf.declared_frames()
    root = world_sdf.to_static_graph(frames)

    cam_link = frames["camera::link"]
    actual = cam_link.transform((0, 0, 0), root)
    expected = (0.8003185305832974, 0.19999974634550793, 1.35)
    assert np.allclose(actual, expected)

    cam_space = frames["camera::link::camera::camera"]
    actual = cam_space.transform((0, 0, 0), root)
    expected = (0.8003185305832974, 0.19999974634550793, 1.35)
    assert np.allclose(actual, expected)


def test_four_goals():
    model_file = Path(__file__).parent / "sdf" / "v18" / "four_goals.sdf"
    sdf_string = model_file.read_text()

    generic_sdf = ign.sdformat.loads_generic(sdf_string)
    world_sdf = generic_sdf.worlds[0]

    static_frames = world_sdf.declared_frames()
    world_sdf.to_static_graph(static_frames)

    px_space = static_frames["main_camera::link::camera::pixel_space"]

    box0 = static_frames["box_copy_0::box_link"]
    box1 = static_frames["box_copy_1::box_link"]
    box2 = static_frames["box_copy_2::box_link"]
    box3 = static_frames["box_copy_3::box_link"]

    center = np.array([0, 0, 0])

    result = box0.transform(center, px_space)
    expected = np.array([1020.82067749, 734.8918789])
    assert np.allclose(result, expected)

    result = box1.transform(center, px_space)
    expected = np.array([992.80649538, 968.49419778])
    assert np.allclose(result, expected)

    result = box2.transform(center, px_space)
    expected = np.array([838.7474601, 835.07845297])
    assert np.allclose(result, expected)

    result = box3.transform(center, px_space)
    expected = np.array([884.74738832, 1026.83742041])
    assert np.allclose(result, expected)

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

    result = box0.transform(vertices, px_space)
    expected = np.array(
        [
            [978.18175552, 767.08033062],
            [1012.11134805, 759.70657528],
            [1029.06133727, 769.14839751],
            [1064.56165032, 761.93590852],
            [978.23390215, 708.56146282],
            [1029.11592056, 711.25700098],
            [1012.16761173, 698.9209838],
            [1064.62049417, 701.82705878],
        ]
    )
    assert np.allclose(result, expected)

    result = box1.transform(vertices, px_space)
    expected = np.array(
        [
            [951.81098295, 996.71126484],
            [983.69175102, 998.18248457],
            [1001.44940597, 996.32944756],
            [1034.82841433, 997.7706284],
            [951.86003774, 939.9670349],
            [1001.5007861, 940.17540062],
            [983.74455559, 939.30942781],
            [1034.88367886, 939.53262033],
        ]
    )
    assert np.allclose(result, expected)

    result = box2.transform(vertices, px_space)
    expected = np.array(
        [
            [806.40774548, 859.888948],
            [828.17240135, 856.87310206],
            [848.88202459, 860.753543],
            [871.75365298, 857.79101721],
            [806.44144929, 812.84770527],
            [848.91745204, 814.11862562],
            [828.20822016, 808.37815077],
            [871.79128351, 809.72777729],
        ]
    )
    assert np.allclose(result, expected)

    result = box3.transform(vertices, px_space)
    expected = np.array(
        [
            [849.89096928, 1051.01033953],
            [874.47255373, 1054.08402528],
            [894.5646881, 1050.17626586],
            [920.36810868, 1053.19371029],
            [849.92896277, 1001.07476015],
            [894.60458206, 1000.69830731],
            [874.51308589, 1002.50722699],
            [920.41064267, 1002.10496116],
        ]
    )
    assert np.allclose(result, expected)

def test_insert_world():
    model_file = (
        Path(__file__).parent / "sdf" / "robots" / "double_pendulum" / "model.sdf"
    )
    sdf_string = model_file.read_text()

    with pytest.raises(ValueError):
        ign.sdformat.to_frame_graph(sdf_string, insert_world_frame=False)