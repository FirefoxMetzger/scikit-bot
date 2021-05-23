from math import exp
import numpy as np
import ropy.transform._utils as util
import pytest


@pytest.mark.parametrize(
    ("v1", "v2", "expected"),
    [
        ((1, 0), (0, 2), np.pi / 2),
        ((0, 2), (1, 0), -np.pi / 2),
        ((1, 1), (0, 1), np.pi / 4),
    ],
)
def test_angle_between(v1, v2, expected):
    result = util.angle_between(v1, v2)
    assert np.isclose(result, expected)
