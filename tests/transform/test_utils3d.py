import pytest
import numpy as np
from scipy.spatial.transform import Rotation as ScipyRotation

import ropy.transform as rtf


@pytest.mark.parametrize(
    "sequence, angles, degrees",
    [
        ("xyz", (0, 0, np.pi/4), False),
        ("xyz", (0, 0, 45), True),
        ("xyz", (0, 0, 90), True),
        ("XZY", (45, 180, 90), True),
        ("XYZ", (45, 180, 90), False),
    ],
)
def test_EulerRotation(sequence, angles, degrees):
    in_vectors = np.eye(3)

    angles = np.asarray(angles)

    rot = rtf.EulerRotation(sequence, angles, degrees=degrees)
    scipy_rot = ScipyRotation.from_euler(sequence, angles, degrees)

    result = rot.transform(in_vectors)
    expected = scipy_rot.apply(in_vectors)

    assert np.allclose(result, expected)


@pytest.mark.parametrize(
    "sequence, quaternion",
    [
        ("xyzw", (0, 1, 0, np.pi)),
        ("xyzw", (1, 0, 0, np.pi/2)),
        ("xyzw", (1, 1, 0, np.pi)),
        ("wxyz", (np.pi, 0, 1, 0)),
        ("wxyz", (np.pi/2, 1, 1, 1)),
    ],
)
def test_QuaternionRotation(sequence, quaternion):
    in_vectors = np.eye(3)

    rot = rtf.QuaternionRotation(quaternion, sequence=sequence)

    if sequence == "xyzw":
        scipy_rot = ScipyRotation.from_quat(quaternion)
    else:
        quaternion = (*quaternion[1:], quaternion[0])
        scipy_rot = ScipyRotation.from_quat(quaternion)

    result = rot.transform(in_vectors)
    expected = scipy_rot.apply(in_vectors)

    assert np.allclose(result, expected)



def test_QuaternionRotation_invalid_sequence():
    with pytest.raises(ValueError):
        rtf.QuaternionRotation((0, 0, 0, 1), sequence="xwyz")

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
