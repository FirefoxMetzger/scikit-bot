import numpy as np
import pytest

import ropy.trajectory as trj


@pytest.mark.parametrize(
    ["t", "f", "expected"],
    [
        [np.linspace(0, 5, 200), lambda x: x, 0.5 * 5 ** 2],
        [np.linspace(0, 5, 500), lambda x: x ** 2, 1 / 3 * 5 ** 3],
        [np.linspace(0, 0, 200), lambda x: x, 0],
    ],
)
def test_integration(t, f, expected):
    f_val = f(t)
    estimate = trj.utils.integral(f_val, t)
    assert np.isclose(estimate, expected)


def test_cumulative_integration():
    t = np.linspace(0, 5, 200)
    f = lambda x: x
    f_val = f(t)
    estimate = trj.utils.cumulative_integral(f_val, t)
    expected = 0.5 * t ** 2
    assert np.allclose(estimate, expected)
