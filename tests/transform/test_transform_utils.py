from math import exp
import numpy as np
import ropy.transform._utils as util
from ropy.transform._utils import angle_between
import pytest


@pytest.mark.parametrize(
    ("v1", "v2", "expected"),
    [
        ((1, 0), (0, 2), np.pi / 2),
        ((0, 2), (1, 0), np.pi / 2),
        ((1, 1), (0, 1), np.pi / 4),
        (
            (
                1,
                0,
                0,
            ),
            (0, 1, 0),
            np.pi / 2,
        ),
        (((1, 0), (2, 0)), ((0, 2), (0, 1)), (np.pi / 2, np.pi / 2)),
    ],
)
def test_angle_between(v1, v2, expected):
    result = util.angle_between(v1, v2)
    assert np.allclose(result, expected)


def test_angle_between_vectorized():
    vec_a = np.eye(3)
    vec_b = vec_a[[1, 2, 0]]
    result = angle_between(vec_a, vec_b)

    assert np.allclose(result, np.pi / 2)


def test_angle_betwee_axis():
    vec_a = np.eye(3).T
    vec_b = vec_a[[1, 2, 0]].T
    result = angle_between(vec_a, vec_b, axis=0)

    assert np.allclose(result, np.pi / 2)

# @pytest.mark.parametrize(
#     ("v1", "v2", "expected"),
#     [
#         ((1, 0), (0, 2), 1),
#         ((0, 2), (1, 0), -1),
#         ((0, 2), (5, 0), -1),
#         ((1, 1), (0, 1), 1),
#         (np.eye(3)[1:, :], np.array((1, 0, 0))[None, :], (-1, 1)),
#         (np.eye(4)[1:, :], np.array((1, 0, 0, 0))[None, :], (-1, 1, 1)),
#         (np.eye(3), np.eye(3)[[1, 2, 1]], (1, 1, 1)),
#         ((0, 1, 0), (1, 0, 0), -1),
#         ((1, 0, 0), (0, 0, 1), 1),
#         ((0, 0, 1), (1, 0, 0), 1),
#         (((1, 0), (2, 0)), ((0, 2), (0, 1)), (1, 1))
#     ],
# )
# def test_angle_between(v1, v2, expected):
#     result = util.rotation_direction(v1, v2)
#     assert np.allclose(result, expected)
