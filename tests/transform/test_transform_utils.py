import numba
import numpy as np
import pytest
import skbot.transform._utils as util
from skbot.transform._utils import angle_between, scalar_project, vector_project, reduce


@pytest.mark.parametrize(
    ("v1", "v2", "expected"),
    [
        ((1, 0), (0, 2), np.pi / 2),
        ((0, 2), (1, 0), np.pi / 2),
        ((1, 1), (0, 1), np.pi / 4),
        (
            (1, 0, 0),
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


def test_angle_between_axis():
    vec_a = np.eye(3).T
    vec_b = vec_a[[1, 2, 0]].T
    result = angle_between(vec_a, vec_b, axis=0)

    assert np.allclose(result, np.pi / 2)


@pytest.mark.parametrize(
    ("vec_A", "vec_B", "expected"),
    [
        ((1, 0), (0, 2), (0, 0)),
        ((1, 0, 0), (0, 1, 0), (0, 0, 0)),
        ((1, 0, 0), ((0, 1, 0), (1, 0, 0)), ((0, 0, 0), (1, 0, 0))),
        (((1, 0), (2, 0), (3, 0), (0, 1)), (0, 1), ((0, 0), (0, 0), (0, 0), (0, 1))),
        (((1, 0), (1, 1)), ((1, 0), (0, 1)), ((1, 0), (0, 1))),
    ],
)
def test_vector_projection(vec_A, vec_B, expected):
    result = vector_project(vec_A, vec_B)
    assert np.allclose(result, expected)


@pytest.mark.parametrize(
    ("vec_A", "vec_B", "expected"),
    [
        ((1, 0), (0, 2), 0),
        ((1, 0, 0), (0, 1, 0), 0),
        ((1, 0, 0), ((0, 1, 0), (1, 0, 0)), (0, 1)),
        (((1, 0), (2, 0), (3, 0), (0, 1)), (0, 1), (0, 0, 0, 1)),
        (((1, 0), (1, 1)), ((1, 0), (0, 1)), (1, 1)),
    ],
)
def test_scalar_projection(vec_A, vec_B, expected):
    result = scalar_project(vec_A, vec_B)
    assert np.allclose(result, expected)


def test_numba_reduce_keepdims():
    # numba_reduce is a pure numba function. It is tested indirectly by calling
    # jitted functions that build on top of it.

    @numba.jit(nopython=True)
    def test_reduce_discard(array):
        return reduce(np.sum, array, axis=-1, keepdims=False)

    @numba.jit(nopython=True)
    def test_reduce_keep(array):
        return reduce(np.sum, array, axis=-1, keepdims=True)

    arr_in = np.arange(10)
    expected = np.sum(arr_in)
    actual = test_reduce_discard(arr_in)

    assert isinstance(actual, int)
    assert np.allclose(actual, expected)

    arr_in = np.arange(10)
    expected = np.sum(arr_in)
    actual = test_reduce_keep(arr_in)

    assert actual.ndim == 1
    assert np.allclose(actual, expected)
