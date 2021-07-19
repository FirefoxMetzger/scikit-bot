import numpy as np
import pytest

import ropy.transform as rtf


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
    projection = rtf.perspective_frustum(fov, im_shape)

    point_cam = rtf.homogenize(point_in)
    point_px = np.matmul(projection, point_cam)

    # this line is not needed here, but it makes sense to touch
    # it during this test
    point_px = rtf.normalize_scale(point_px)

    point_px = rtf.cartesianize(point_px)

    assert np.allclose(point_px, point_out)


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
def test_perspective_transform(point_in, fov, im_shape, point_out):
    proj = rtf.projections.PerspectiveProjection(fov, im_shape)
    assert np.allclose(proj.transform(point_in), point_out)


@pytest.mark.parametrize(
    "parent_coords, child_coords, direction, amount",
    [
        ((1, 1, 0), 1, (1, 0, 0), (0, 1, 0)),
        ((1, 1), 0.25, (4, 0), (0, 1)),
        ((4, 1), 1, (4, 0), (0, 1)),
    ],
)
def test_1d_projections(parent_coords, child_coords, direction, amount):
    proj = rtf.projections.NDPerspectiveProjection(direction, amount)
    result = proj.transform(parent_coords)
    assert np.allclose(result, child_coords)
