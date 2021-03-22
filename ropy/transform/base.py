import numpy as np
from math import sin, cos


def _homogenize(cartesian_vector: np.array) -> np.array:
    """Convert a vector from cartesian coordinates into homogeneous coordinates.

    Parameters
    ----------
    cartesian_vector: np.array
        The vector to be converted.

    Returns
    -------
    homogeneous_vector: np.array
        The vector in homogeneous coordinates.

    """
    cartesian_vector = np.asarray(cartesian_vector)

    shape = cartesian_vector.shape
    homogeneous_vector = np.ones((*shape[:-1], shape[-1] + 1))
    homogeneous_vector[..., :-1] = cartesian_vector
    return homogeneous_vector


def _cartesianize(homogeneous_vector: np.array) -> np.array:
    """Convert a vector from homogeneous coordinates to cartesian coordinates.

    Parameters
    ----------
    homogeneous_vector: np.array
        The vector in homogeneous coordinates.

    Returns
    -------
    cartesian_vector: np.array
        The vector to be converted.

    """

    return homogeneous_vector[..., :-1] / homogeneous_vector[..., -1]


def normalize_scale(vector: np.array) -> np.array:
    """Return an equivalent homogeneous vector with scale set to 1.

    Parameters
    ----------
    vector: np.array
        The vector (in homogeneous coordinates) to be scale-normalized.
    
    Returns
    -------
    vector: np.array
        An equivalent vector with scale component set to 1.

    """

    vector = np.asarray(vector)

    return vector / vector[-1]


def rotation_matrix(angle: float, u: np.array, v: np.array) -> np.array:
    """Returns a matrix rotating the span of u and v by the given angle.

    Parameters
    ----------
    angle: float
        The amount (in radians) by which to rotate the plane.
    u: np.array
        One of two orthonormal basis vectors (u,v) that span the plane
        in which the rotation takes place. The vector is given in
        homogeneous coordinates.
    v: np.array
        One of the two orthonormal basis vectors (u,v) that span the plane
        in which the rotation takes place. The vector is given in
        homogeneous coordinates.

    Returns
    -------
    rotation_matrix: np.array
        A matrix representing the rotation in cartesian coordinates.
    """

    # This implementation is based on a very insightful stackoverflow
    # comment
    # https://math.stackexchange.com/questions/197772/generalized-rotation-matrix-in-n-dimensional-space-around-n-2-unit-vector#comment453048_197778
    
    u = _cartesianize(np.asarray(u))
    v = _cartesianize(np.asarray(v))

    ndim = u.size

    rotation_matrix = np.eye(ndim)
    rotation_matrix += sin(angle)*(np.outer(v, u)-np.outer(u, v))
    rotation_matrix += (cos(angle) - 1)*(np.outer(u, u)+np.outer(v, v))

    return rotation_matrix


# other candidates for base functions:
# https://www.javatpoint.com/computer-graphics-homogeneous-coordinates
# (mainly for my own reference)
