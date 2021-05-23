import numpy as np
from math import sin, cos
from numpy.typing import ArrayLike


def scale(vector: ArrayLike, scalar: ArrayLike) -> np.ndarray:
    """Scale each dimension of a homogeneous vector individually.

    Multiplies each dimension of the homogeneous vector ``vector`` with
    the matching dimension of the cartesian vector ``scalar``. If necessary,
    ``scalar`` will be broadcasted.

    Parameters
    ----------
    vector : ArrayLike
        A homogeneous vector to be scaled.
    scalar : ArrayLike
        A cartesian vector representing the amount by which to scale each dimension.

    Returns
    -------
    scaled : ArrayLike
        A homogeneous vector where each dimension is scaled by scalar.

    """
    vector = np.asarray(vector)

    scaled = vector
    scaled[:-1] *= scalar

    return scaled


def scale_uniform(vector: ArrayLike, scalar: float) -> np.ndarray:
    """Scale a homogeneous vector by a scalar.

    Multiplies the scale portion of the homogeneous vector by scalar.
    This is faster (and potentially more accurate) than ``scale`` if each
    dimension is scaled by the same amount.

    Parameters
    ----------
    vector : ArrayLike
        A homogeneous vector to be scaled.
    scalar : float
        The amount by which to scale.

    Returns
    -------
    scaled : ArrayLike
        A homogeneous vector where each dimension is scaled by scalar.

    """
    vector = np.asarray(vector)

    scaled = vector
    scaled[-1] *= scalar

    return scaled


def translate(vector: ArrayLike, direction: ArrayLike) -> np.ndarray:
    """Translate a vector along direction.

    Parameters
    ----------
    vector : ArrayLike
        The vector to be translated.
    direction : ArrayLike
        A vector describing the translation.

    Returns
    -------
    translated_vector : ArrayLike
        The translated vector.

    Notes
    -----
    Exists for completeness. It may be cleaner to simply write
    ``vector + direction`` instead.

    """

    return vector + direction


def rotate(vector: ArrayLike, u: ArrayLike, v: ArrayLike) -> np.ndarray:
    """Rotate a vector in the u,v plane.

    Rotates a vector by reflecting it twice. The plane of rotation
    is given by the u-v-plane and the angle of rotation is two times
    the angle from u to v.

    Parameters
    ----------
    vector : ArrayLike
        The vector to be rotated.
    u : ArrayLike
        The first of the two axes defining the plane of rotation
    v : ArrayLike
        The second of the two axes defining the plane of rotation

    Returns
    -------
    rotated_vector : np.ndarray
        The vector rotated in the u-v-plane by two times the angle
        from u to v.

    Notes
    -----
    The angle of rotation is given by the angle between the two vectors that
    define the plane of rotation. The orientation of the rotation is from u
    towards v, and the amount of rotation is twice the angle.

    The scale of u and/or v does not influence the rotation.

    """

    vector = np.asarray(vector)
    u = np.asarray(u)
    v = np.asarray(v)

    # implemented as rotation by two reflections
    return reflect(reflect(vector, u), v)


def reflect(vector: ArrayLike, direction: ArrayLike) -> np.ndarray:
    """Reflect a vector along a line defined by direction.

    Parameters
    ----------
    vector : ArrayLike
        The vector to be reflected.
    direction : ArrayLike
        The direction along which the reflection takes place.

    Returns
    -------
    reflected_vector : ArrayLike
        The reflected vector.

    Notes
    -----
    The length of direction does not influence the result of the reflection.

    """

    # from: https://en.wikipedia.org/wiki/Reflection_(mathematics)#Reflection_through_a_hyperplane_in_n_dimensions
    vector = np.asarray(vector)
    direction = np.asarray(direction)

    return (
        vector
        - 2 * np.dot(vector, direction) / np.dot(direction, direction) * direction
    )


def shear(vector: ArrayLike, direction: ArrayLike, amount: ArrayLike) -> np.ndarray:
    """Displaces a vector along direction by the scalar product of vector and amount.

    A shear displaces a vector in a fixed direction by the vector's scalar
    projection onto a second vector (amount) scaled by the length of that second
    vector. If amount and direction are orthogonal, the result is a shear. If
    amount and direction are parallel, the result is a stretch.

    Parameters
    ----------
    vector : ArrayLike
        The vector to be sheared.
    direction : ArrayLike
        The direction along which to apply the shear.
    amount : ArrayLike
        The axis that determines the amount to shear by.

    Returns
    -------
    sheared : np.ndarray
        The sheared vector.

    Notes
    -----
    If direction is not normalized the resulting shear factor will be scaled by
    the length (euclidian norm) of direction.

    """

    vector = np.asarray(vector)
    direction = np.asarray(direction)
    amount = np.asarray(amount)

    return vector + np.dot(vector, amount) * direction
