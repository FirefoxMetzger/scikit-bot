import pytest
import numpy as np

import ropy.ignition as ign


@pytest.mark.parametrize(
    "point_in, fov, im_shape, point_out",
    [
        ((1, 0, 0), np.pi / 3, (240, 320), (120, 160)),
        ((3.5, 0, 0), np.pi / 2, (240, 320), (120, 160)),
        ((1, 0, 0), 1.5 * np.pi, (480, 640), (240, 320)),
        ((1, 1, 480 / 640), np.pi / 2, (480, 640), (480, 640)),
        ((1, -1, -480 / 640), np.pi / 2, (480, 640), (0, 0)),
    ],
)
def test_perspective_transform(point_in, fov, im_shape, point_out):
    proj = ign.FrustumProjection(fov, im_shape)
    assert np.allclose(proj.transform(point_in), point_out)
