import pytest
import skbot.transform as tf
import numpy as np
from numpy.typing import ArrayLike
from typing import List


def test_compound_unwrapping():
    points = np.arange(200 * 3).reshape(200, 3)

    link = tf.CompundLink(
        [
            tf.Translation((1, 0, 0)),
            tf.CompundLink(
                [
                    tf.Translation((0, 1, 0)),
                ]
            ),
            tf.EulerRotation("Y", -90, degrees=True),
        ]
    )
    simplified_links = tf.simplify_links([link])

    expected = link.transform(points)
    result = points
    for link in simplified_links:
        assert not isinstance(link, tf.CompundLink)
        result = link.transform(result)
    assert np.allclose(result, expected)


def test_identity_drops():
    link = tf.Rotation((1, 0, 0), (0, 1, 0))
    link.angle = 0
    simplified_links = tf.simplify_links([link])
    assert len(simplified_links) == 0

    link = tf.EulerRotation("XYZ", (0, 0, 0))
    simplified_links = tf.simplify_links([link])
    assert len(simplified_links) == 0

    link = tf.Translation((1, 2, 3), amount=0)
    simplified_links = tf.simplify_links([link])
    assert len(simplified_links) == 0


def test_inverse_links():
    points = np.arange(200 * 3).reshape(200, 3)

    # --- test double_inverse ---
    link = tf.InvertLink(tf.InvertLink(tf.Translation((1, 0, 0))))
    simplified = tf.simplify_links([link])[0]

    assert isinstance(simplified, tf.Translation)

    expected = link.transform(points)
    result = simplified.transform(points)
    assert np.allclose(result, expected)

    # --- test translation unwrapping ---
    link = tf.InvertLink(tf.Translation((1, 0, 0)))
    simplified = tf.simplify_links([link])[0]

    assert isinstance(simplified, tf.Translation)

    expected = link.transform(points)
    result = simplified.transform(points)
    assert np.allclose(result, expected)

    # --- test rotation unwrapping ---
    link = tf.InvertLink(tf.EulerRotation("X", np.pi / 2))
    simplified = tf.simplify_links([link])[0]

    assert isinstance(simplified, tf.Rotation)

    expected = link.transform(points)
    result = simplified.transform(points)
    assert np.allclose(result, expected)

    # --- test compound unpacking ---
    link = tf.InvertLink(
        tf.CompundLink([tf.Translation((1, 0, 0)), tf.Translation((0, 1, 0))])
    )
    simplified_links = tf.simplify_links([link])

    expected = link.transform(points)
    result = points
    for link in simplified_links:
        result = link.transform(result)
    assert np.allclose(result, expected)

    for link in simplified_links:
        assert isinstance(link, tf.Translation)


def test_keep_link():
    points = np.arange(200 * 3).reshape(200, 3)

    keep_link = tf.Translation((0, 1, 0))
    link = tf.CompundLink(
        [
            tf.Translation((1, 0, 0)),
            tf.CompundLink([keep_link]),
            tf.EulerRotation("Y", -90, degrees=True),
        ]
    )
    simplified_links = tf.simplify_links([link], keep_links=[keep_link])

    assert keep_link in simplified_links

    expected = link.transform(points)
    result = points
    for link in simplified_links:
        result = link.transform(result)
    assert np.allclose(result, expected)

    keep_link = tf.Translation((0, 1, 0))
    original_link = tf.CompundLink(
        [
            tf.Translation((1, 0, 0)),
            tf.CompundLink([tf.InvertLink(keep_link)]),
            tf.EulerRotation("Y", -90, degrees=True),
        ]
    )
    simplified_links = tf.simplify_links([original_link], keep_links=[keep_link])

    for link in simplified_links:
        if isinstance(link, tf.InvertLink):
            if link._forward_link is keep_link:
                break
    else:
        raise AssertionError("`keep_link` no longer in link chain.")

    expected = original_link.transform(points)
    result = points
    for link in simplified_links:
        result = link.transform(result)
    assert np.allclose(result, expected)

    keep_link = tf.Translation((0, 1, 0))
    original_link = tf.CompundLink(
        [
            tf.Translation((1, 0, 0)),
            tf.Translation((1, 1, 0)),
            keep_link,
            tf.EulerRotation("Y", -90, degrees=True),
        ]
    )
    simplified_links = tf.simplify_links([original_link], keep_links=[keep_link])

    assert keep_link in simplified_links

    expected = original_link.transform(points)
    result = points
    for link in simplified_links:
        result = link.transform(result)
    assert np.allclose(result, expected)


def test_combine_translation():
    points = np.arange(200 * 3).reshape(200, 3)

    link = tf.CompundLink(
        [
            tf.Translation((1, 0, 0)),
            tf.CompundLink([tf.Translation((0, 1, 0))]),
        ]
    )
    simplified_links = tf.simplify_links([link])
    assert len(simplified_links) == 1

    simple_link = simplified_links[0]
    assert isinstance(simple_link, tf.Translation)
    assert simple_link._amount == 1
    assert np.allclose(simple_link._direction, (1, 1, 0))

    expected = link.transform(points)
    result = simple_link.transform(points)
    assert np.allclose(result, expected)

    link = tf.CompundLink(
        [
            tf.Translation((1, 0, 0)),
            tf.CompundLink(
                [tf.Translation((0, 1, 0)), tf.Translation((0, 0, 1), amount=0.3)]
            ),
            tf.Translation((0.2, 0, 0), amount=0.5),
        ]
    )
    simplified_links = tf.simplify_links([link])
    assert len(simplified_links) == 1

    simple_link = simplified_links[0]
    assert isinstance(simple_link, tf.Translation)
    assert simple_link._amount == 1
    assert np.allclose(simple_link._direction, (1.1, 1, 0.3))

    expected = link.transform(points)
    result = simple_link.transform(points)
    assert np.allclose(result, expected)


def test_inverted_custom_link():
    class Custom(tf.Link):
        def transform(self, x: ArrayLike) -> np.ndarray:
            return x

        def __inverse_transform__(self, x: ArrayLike) -> np.ndarray:
            return x

    points = np.arange(200 * 3).reshape(200, 3)

    link = tf.InvertLink(Custom(3, 3))
    simplified_links = tf.simplify_links([link])

    expected = link.transform(points)
    result = points
    for link in simplified_links:
        result = link.transform(result)
    assert np.allclose(result, expected)


def test_link_ordering():
    points = np.arange(200 * 3).reshape(200, 3)

    links: List[tf.Link] = [
        tf.Rotation((1, 0, 0), (0, 1, 0)),
        tf.Translation((1, 0, 0)),
        tf.Translation((1, 1, 0)),
        tf.Translation((1, 1, 1)),
    ]
    simplified_links = tf.simplify_links(links)

    expected = points
    for link in links:
        expected = link.transform(expected)
    result = points
    for link in simplified_links:
        result = link.transform(result)
    assert np.allclose(result, expected)

    assert isinstance(simplified_links[-1], tf.Rotation)


def test_keep_joints():
    points = np.arange(200 * 3).reshape(200, 3)

    joint1 = tf.RotationalJoint((0, 1, 0))
    joint2 = tf.PrismaticJoint((1, 0, 0))

    links: List[tf.Link] = [
        tf.Rotation((1, 0, 0), (0, 1, 0)),
        tf.Translation((1, 0, 0)),
        joint1,
        tf.Translation((1, 1, 0)),
        tf.Translation((1, 1, 1)),
        tf.InvertLink(joint2),
    ]
    simplified_links = tf.simplify_links(links)

    expected = points
    for link in links:
        expected = link.transform(expected)
    result = points
    for link in simplified_links:
        result = link.transform(result)
    assert np.allclose(result, expected)

    assert joint1 in simplified_links
    assert joint2 is simplified_links[-1]._forward_link
