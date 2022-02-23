import numpy as np

import skbot.transform as tf


def test_axisHex():
    hex_coords = np.repeat(np.arange(-5, 5)[:, None], 2, axis=-1)

    expected = np.array(
        [
            [-7.5, -12.99038106],
            [-6.0, -10.39230485],
            [-4.5, -7.79422863],
            [-3.0, -5.19615242],
            [-1.5, -2.59807621],
            [0.0, 0.0],
            [1.5, 2.59807621],
            [3.0, 5.19615242],
            [4.5, 7.79422863],
            [6.0, 10.39230485],
        ]
    )
    hex_transform = tf.AxialHexagonTransform()
    inverse_hex = tf.InvertLink(hex_transform)
    actual = inverse_hex.transform(hex_coords)
    assert np.allclose(actual, expected)

    actual = hex_transform.transform(actual)
    assert np.allclose(actual, hex_coords)

    expected = np.array(
        [
            [-37.5, -64.95190528],
            [-30.0, -51.96152423],
            [-22.5, -38.97114317],
            [-15.0, -25.98076211],
            [-7.5, -12.99038106],
            [0.0, 0.0],
            [7.5, 12.99038106],
            [15.0, 25.98076211],
            [22.5, 38.97114317],
            [30.0, 51.96152423],
        ]
    )
    hex_transform = tf.AxialHexagonTransform(size=5)
    inverse_hex = tf.InvertLink(hex_transform)
    actual = inverse_hex.transform(hex_coords)
    assert np.allclose(actual, expected)
    actual = hex_transform.transform(actual)
    assert np.allclose(actual, hex_coords)

    expected = np.array(
        [
            [-12.99038106, -7.5],
            [-10.39230485, -6.0],
            [-7.79422863, -4.5],
            [-5.19615242, -3.0],
            [-2.59807621, -1.5],
            [0.0, 0.0],
            [2.59807621, 1.5],
            [5.19615242, 3.0],
            [7.79422863, 4.5],
            [10.39230485, 6.0],
        ]
    )
    hex_transform = tf.AxialHexagonTransform(flat_top=False)
    inverse_hex = tf.InvertLink(hex_transform)
    actual = inverse_hex.transform(hex_coords)
    assert np.allclose(actual, expected)
    actual = hex_transform.transform(actual)
    assert np.allclose(actual, hex_coords)
