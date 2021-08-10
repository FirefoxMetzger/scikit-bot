import numpy as np
import pytest

import skbot.transform as tf


@pytest.mark.parametrize(
    "parent_coords, child_coords, direction, amount",
    [
        ((1, 1, 0), 1, ((1, 0, 0),), ((0, 1, 0),)),
        ((1, 1), 0.25, ((4, 0),), ((0, 1),)),
        ((4, 1), 1, ((4, 0),), ((0, 1),)),
    ],
)
def test_1d_projections(parent_coords, child_coords, direction, amount):
    proj = tf.projections.PerspectiveProjection(direction, amount)
    result = proj.transform(parent_coords)
    assert np.allclose(result, child_coords)
