import pytest
import numpy as np
from scipy.spatial.transform import Rotation as ScipyRotation

import skbot.transform as tf


@pytest.mark.parametrize(
    "rotvec, angle, degrees, axis",
    [
        ((0, 0, 1), np.pi / 2, False, -1),
        ((4, 6, 0), np.pi / 3, False, -1),
        ((0, 0, 1), 90, True, -1),
        ((0, 0, 1), 43, True, -1),
        ((1, 1, 0), 180, True, -1),
        ((0, 0, 1), 0, False, -1),
        ((0, 0, 90), None, True, -1),
        ((0, 0, np.pi / 3), None, False, -1),
    ],
)
def test_RotvecRotation(rotvec, angle, degrees, axis):
    in_vectors = np.eye(3)

    rot = tf.RotvecRotation(rotvec, angle=angle, degrees=degrees, axis=axis)
    result = rot.transform(in_vectors)

    rotvec = np.asarray(rotvec, dtype=np.float_)

    if angle is not None:
        angle = np.asarray(angle)
        rotvec *= angle / np.linalg.norm(rotvec, axis=axis)

    rotvec = np.moveaxis(rotvec, axis, -1)
    scipy_rot = ScipyRotation.from_rotvec(rotvec, degrees)
    expected = scipy_rot.apply(in_vectors)
    expected = np.moveaxis(expected, -1, axis)

    assert np.allclose(result, expected)


@pytest.mark.parametrize(
    "rotvec, angle, degrees, axis",
    [
        ((((1, 0, 0), (0, 1, 0)),), np.pi / 2, False, -1),
        ((((1, 0, 0), (0, 1, 0)),), ((np.pi / 2, np.pi / 3),), False, -1),
        (np.eye(3).reshape(3, 1, 3), np.pi / 2, False, 0),
    ],
)
def test_vectorized_RotvecRotation(rotvec, angle, degrees, axis):
    in_vectors = np.eye(3)
    in_vectors = np.expand_dims(in_vectors, 1)

    rotvec = np.asarray(rotvec, dtype=np.float_)
    angle = np.asarray(angle)

    rot = tf.RotvecRotation(rotvec, angle=angle, degrees=degrees, axis=axis)
    result = rot.transform(in_vectors)

    rotvec = np.moveaxis(rotvec, axis, -1)
    scaling = angle / np.linalg.norm(rotvec, axis=-1)
    rotvec *= scaling[..., None]
    scipy_rot = ScipyRotation.from_rotvec(rotvec[0], degrees)
    batch = list()
    for vec in in_vectors:
        batch.append(scipy_rot.apply(vec))
    expected = np.stack(batch, axis=0)
    expected = np.moveaxis(expected, -1, axis)

    assert np.allclose(result, expected)


@pytest.mark.parametrize(
    "sequence, angles, degrees",
    [
        ("xyz", (0, 0, np.pi / 4), False),
        ("xyz", (0, 0, 45), True),
        ("xyz", (0, 0, 90), True),
        ("XZY", (45, 180, 90), True),
        ("XYZ", (np.pi/4, np.pi, np.pi/2), False),
    ],
)
def test_EulerRotation(sequence, angles, degrees):
    in_vectors = np.eye(3)

    angles = np.asarray(angles)

    rot = tf.EulerRotation(sequence, angles, degrees=degrees)
    scipy_rot = ScipyRotation.from_euler(sequence, angles, degrees)

    result = rot.transform(in_vectors)
    expected = scipy_rot.apply(in_vectors)

    assert np.allclose(result, expected)


@pytest.mark.parametrize(
    "sequence, angles, degrees",
    [
        ("xyz", ((0, 0, np.pi / 4),(0, 0, 0)), False),
        ("xyz", ((0, 0, 45),), True),
        ("xyz", ((0, 0, 90),(0, 90, 0), (0, 0, 90)), True),
        ("XZY", ((45, 180, 90),(20, 63, 176)), True),
        ("XYZ", ((np.pi/4, np.pi, np.pi/2),(np.pi/6, 3/2*np.pi, 3*np.pi)), False),
    ],
)
def test_EulerRotation_vectorized(sequence, angles, degrees):
    angles = np.asarray(angles)
    
    in_vectors = np.eye(3)

    rot = tf.EulerRotation(sequence, angles[None, ...], degrees=degrees)
    scipy_rot = ScipyRotation.from_euler(sequence, angles, degrees)

    result = rot.transform(in_vectors[:, None, :])

    expected = list()
    for basis in in_vectors:
        partial = scipy_rot.apply(basis)
        expected.append(partial)
    expected = np.stack(expected, axis=0)

    assert np.allclose(result, expected)


@pytest.mark.parametrize(
    "sequence",
    [
        "XyZ",
        "abc",
        "xyw"
    ],
)
def test_EulerRotation_invalid_sequence(sequence):
    with pytest.raises(ValueError):
        tf.EulerRotation(sequence, (0, 0, 0))

@pytest.mark.parametrize(
    "sequence, quaternion",
    [
        ("xyzw", (0, 1, 0, np.pi)),
        ("xyzw", (1, 0, 0, np.pi / 2)),
        ("xyzw", (1, 1, 0, np.pi)),
        ("wxyz", (np.pi, 0, 1, 0)),
        ("wxyz", (np.pi / 2, 1, 1, 1)),
    ],
)
def test_QuaternionRotation(sequence, quaternion):
    in_vectors = np.eye(3)

    rot = tf.QuaternionRotation(quaternion, sequence=sequence)

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
        tf.QuaternionRotation((0, 0, 0, 1), sequence="xwyz")


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
    proj = tf.FrustumProjection(fov, im_shape)
    assert np.allclose(proj.transform(point_in), point_out)
