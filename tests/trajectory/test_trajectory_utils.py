import numpy as np
import pytest

import ropy.trajectory as trj


@pytest.mark.parametrize(
    ["t", "f", "expected"],
    [
        [np.linspace(0, 5, 200), lambda x: x, 0.5 * 5 ** 2],
        [np.linspace(0, 5, 500), lambda x: x ** 2, 1 / 3 * 5 ** 3],
    ],
)
def test_integration(t, f, expected):
    f_val = f(t)
    estimate = trj.utils.discrete_integral(f_val, t)
    assert np.isclose(estimate, expected)


def test_integration_none():
    f_val = np.linspace(0, 1, 300) ** 2
    estimate = trj.utils.discrete_integral(f_val)
    expected = 1 / 3
    assert np.isclose(estimate, expected)
