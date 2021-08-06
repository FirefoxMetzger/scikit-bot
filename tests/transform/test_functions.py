import numpy as np
import skbot.transform as rtf
import pytest


@pytest.mark.parametrize(
    ("vector", "direction", "amount", "expected"),
    [
        ((1, 1), (0, 1), (1, 0), (1, 2)),
        ((1, 1, 0), (0, 0, 1), (1, 0, 0), (1, 1, 1)),
        ((1, 1, 0), (0, 0, 1), (1, 1, 0), (1, 1, 2)),
        (
            (1, 1, 1, 0, 0, 0),
            (0, 0, 0, 0, 1, 1),
            (1, 1, 0, 0, 0, 0),
            (1, 1, 1, 0, 2, 2),
        ),
    ],
)
def test_shear(vector, direction, amount, expected):
    result = rtf.shear(vector, direction, amount)
    assert np.allclose(result, expected)


@pytest.mark.parametrize(
    ("vector", "scalar", "expected"),
    [
        ((1, 1), (1, 2), (1, 2)),
        ((1, 1, 0), (1, 2, 3), (1, 2, 0)),
        ((1, 1, 1, 0, 0, 0), (0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 0, 0)),
    ],
)
def test_scale(vector, scalar, expected):
    result = rtf.scale(vector, scalar)
    assert np.allclose(result, expected)
