from pathlib import Path
import numpy as np

import ropy.ignition as ign


def test_sdformat():
    # actually no assert right now, but a stub for me to debug the parser
    with open(Path(__file__).parent / "panda_world.sdf", "r") as file:
        sdf_string = file.read()

    foo = ign.create_frame_graph(sdf_string)


def test_light(light_sdf):
    frames, links = ign.create_frame_graph(light_sdf)

    # check if all frames were created
    assert all(key in frames.keys() for key in ["/sdf", "/sdf/point_light"])

    # check if the origin is where it belongs
    result = frames["/sdf/point_light"].transform((0, 0, 0), "/sdf")
    expected = (0, 2, 2)
    assert np.allclose(result, expected)
