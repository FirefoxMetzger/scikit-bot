import pytest
import skbot.transform as tf
import numpy as np


def test_prismatic():
    joint = tf.PrismaticJoint((1, 0, 0), upper_limit=10, lower_limit=0)

    expected = (1, 0, 0)
    result = joint.transform((0, 0, 0))
    assert np.allclose(expected, result)

    joint.amount = 5
    assert joint.param == 5

    expected = (5, 0, 0)
    result = joint.transform((0, 0, 0))
    assert np.allclose(expected, result)


def test_prismatic_out_of_bounds():
    joint = tf.PrismaticJoint((0, 0, 1))

    with pytest.raises(ValueError):
        joint.amount = 10


def test_rotational_out_of_bounds():
    joint = tf.RotationalJoint((0, 0, 1), angle=90, degrees=True)

    with pytest.raises(ValueError):
        joint.angle = -45
