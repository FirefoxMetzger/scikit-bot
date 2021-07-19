import pytest
import numpy as np

import ropy.transform as rtf


@pytest.mark.parametrize(
    "point_in, fov, im_shape, point_out",
    [
        ((0, 0, 1), np.pi / 3, (240, 320), (120, 160)),
        ((0, 0, 3.5), np.pi / 2, (240, 320), (120, 160)),
        ((0, 0, 1), 1.5 * np.pi, (480, 640), (240, 320)),
        ((480 / 640, 1, 1), np.pi / 2, (480, 640), (480, 640)),
        ((-480 / 640, -1, 1), np.pi / 2, (480, 640), (0, 0)),
    ],
)
def test_perspective_transform(point_in, fov, im_shape, point_out):
    proj = rtf.FrustumProjection(fov, im_shape)
    assert np.allclose(proj.transform(point_in), point_out)
