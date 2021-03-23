import numpy as np
import pytest

import ropy.transform as tf


@pytest.mark.parametrize(
    "vector_in,frame,vector_out",
    [
        ((1, 2, 3), (1, 2, 3, 0, 0, 0), (0, 0, 0)),
        ((1, 0, 0), (0, 0, 0, 0, 0, np.pi / 2), (0, -1, 0)),
        ((0, 1, 0), (0, 0, 0, np.pi / 2, 0, np.pi / 2), (0, 0, -1)),
    ],
)
def test_transform(vector_in, frame, vector_out):
    vector_A = tf.homogenize(vector_in)
    vector_B = np.matmul(tf.coordinates.transform(frame), vector_A)
    vector_B = tf.cartesianize(vector_B)

    assert np.allclose(vector_B, vector_out)


@pytest.mark.parametrize(
    "vector_in,frame,vector_out",
    [
        ((0, 0, 0), (1, 2, 3, 0, 0, 0), (1, 2, 3)),
        ((0, -1, 0), (0, 0, 0, 0, 0, np.pi / 2), (1, 0, 0)),
        ((0, 0, -1), (0, 0, 0, np.pi / 2, 0, np.pi / 2), (0, 1, 0)),
    ],
)
def test_inverse_transform(vector_in, frame, vector_out):
    vector_A = tf.homogenize(vector_in)
    vector_B = np.matmul(tf.coordinates.inverse_transform(frame), vector_A)
    vector_B = tf.cartesianize(vector_B)

    assert np.allclose(vector_B, vector_out)


@pytest.mark.parametrize(
    "vector_in,frame_A,frame_B,vector_out",
    [
        (
            (0, np.sqrt(2), 0),
            (0, 0, 0, 0, 0, -np.pi / 4),
            (1, 1, 0, 0, 0, 0),
            (0, 0, 0),
        ),
    ],
)
def test_transform_between(vector_in, frame_A, frame_B, vector_out):
    vector_A = tf.homogenize(vector_in)
    vector_B = np.matmul(tf.coordinates.transform_between(frame_A, frame_B), vector_A)
    vector_B = tf.cartesianize(vector_B)

    assert np.allclose(vector_B, vector_out)


@pytest.mark.parametrize(
    "frame",
    [
        np.array((0, 0, 0, 0, 0, 0)),
        (1, 0, 0, 0, 0, 0),
        [0, 0, 0, 0, 0, np.pi / 2],
        (4.5, 1, 0, 0, 0, -np.pi / 4),
    ],
)
def test_identity(frame):
    A = tf.coordinates.transform(frame)
    B = tf.coordinates.inverse_transform(frame)
    assert np.allclose(np.matmul(B, A), np.eye(4))
