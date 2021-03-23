import numpy as np
import pytest

import ropy.transform as tf


@pytest.mark.parametrize(
    "point_in, fov, im_shape, point_out",
    [
        ((1, 0, 0), np.pi / 3, (240, 320), (160, 120)),
        ((3.5, 0, 0), np.pi / 2, (240, 320), (160, 120)),
        ((1, 0, 0), 1.5 * np.pi, (480, 640), (320, 240)),
        ((1, 1, 480 / 640), 1.5 * np.pi, (480, 640), (640, 480)),
        ((1, -1, -480 / 640), 1.5 * np.pi, (480, 640), (0, 0)),
    ],
)
def test_frustum_project(point_in, fov, im_shape, point_out):
    projection = tf.projections.camera_frustum(fov, im_shape)

    point_cam = tf.homogenize(point_in)
    point_px = np.matmul(projection, point_cam)

    # this line is not needed here, but it makes sense to touch
    # it during this test
    point_px = tf.base.normalize_scale(point_px)

    point_px = tf.cartesianize(point_px)

    assert np.allclose(point_px, point_out)
