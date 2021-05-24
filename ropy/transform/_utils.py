import numpy as np
from math import sqrt, atan, sin, cos
from numpy.typing import ArrayLike


def vector_project(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    """Returns the component of a along b."""

    a = np.asarray(a)
    b = np.asarray(b)

    return np.dot(a, b) / np.dot(b, b) * b


def angle_between(vec_a: ArrayLike, vec_b: ArrayLike) -> float:
    """Computes the signed angle from a to b (in a right-handed frame)

    Notes
    -----
    Implementation is based on this StackOverflow post:
    https://scicomp.stackexchange.com/a/27694
    """

    vec_a = np.asarray(vec_a)
    vec_b = np.asarray(vec_b)

    len_c = np.linalg.norm(vec_a - vec_b)
    len_a = np.linalg.norm(vec_a)
    len_b = np.linalg.norm(vec_b)

    flipped = 1

    if len_a < len_b:
        flipped *= -1
        len_a, len_b = len_b, len_a

    if len_c > len_b:
        flipped *= -1
        mu = len_b - (len_a - len_c)
    else:
        mu = len_c - (len_a - len_b)

    numerator = ((len_a - len_b) + len_c) * mu
    denominator = (len_a + (len_b + len_c)) * ((len_a - len_c) + len_b)

    if denominator == 0 and numerator > 0:
        return flipped * np.pi

    angle = 2 * atan(sqrt(numerator / denominator))

    return flipped * angle


def rotvec_to_reflections(rotvec: ArrayLike, *, angle: float = None) -> np.ndarray:
    """Compute the reflection vectors from a rotation vector.

    Given a rotation vector in 3D, that is a vector that is orthogonal to the
    plane of rotation and who's magnitude describes the angle (in radians) of
    rotation, compute the two reflection vectors that - when applied iteratively
    - result in the same rotation as described by the vector.


    Parameters
    ----------
    rotvec : ArrayLike
        The rotation vector.
    angle : ArrayLike
        An optional angle of rotation. If not None the magnitude of rotvec has no effect.

    Returns
    -------
    u : np.ndarray
        The first reflection vector.
    v : np.ndarray
        The second reflection vector.

    """

    rotvec = np.asarray(rotvec)

    if angle is None:
        angle = np.linalg.norm(rotvec)

    # arbitrary vector that isn't parallel to rotvec
    tmp_vector = np.array((1, 0, 0), dtype=np.float_)
    enclosing_angle = abs(angle_between(tmp_vector, rotvec))
    if enclosing_angle < np.pi / 4 or abs(enclosing_angle - np.pi) < np.pi / 4:
        tmp_vector = np.array((0, 1, 0), dtype=np.float_)

    vec_u = tmp_vector - vector_project(tmp_vector, rotvec)
    basis2 = np.cross(vec_u, rotvec)
    basis2 /= np.linalg.norm(basis2)

    vec_v = cos(angle / 2) * vec_u + sin(angle / 2) * basis2

    return vec_u, vec_v
