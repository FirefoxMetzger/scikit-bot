import numpy as np
import ropy.trajectory as rtj
import pytest


@pytest.mark.parametrize(
    "t,t_out,t_min,t_max",
    [
        (0, [1, 2, 3], 0, 1),
        (1, [6, 7, 8], 0, 1),
        (1.5 / 5, [2.5, 3.5, 4.5], 0, 1),
        (3, [3.5, 4.5, 5.5], -2, 8),
    ],
)
def test_even_spacing(t, t_out, t_min, t_max):
    control_points = np.array(
        [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8]]
    )

    estimate = rtj.spline(t, control_points, t_min=t_min, t_max=t_max)
    assert np.allclose(estimate, t_out)


@pytest.mark.parametrize(
    "t,t_out,t_k",
    [
        (0, (1, 2, 3), (0, 0.3, 0.5, 0.55, 0.75, 1)),
        (0.5, (3, 4, 5), (0, 0.3, 0.5, 0.55, 0.75, 1)),
        (0.75, (5, 6, 7), (0, 0.3, 0.5, 0.55, 0.75, 1)),
    ],
)
def test_custom_spacing(t, t_out, t_k):
    control_points = np.array(
        [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8]]
    )

    estimate = rtj.spline(t, control_points, t_control=t_k)
    assert np.allclose(estimate, t_out)
