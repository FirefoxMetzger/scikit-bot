import numpy as np
from math import sin, cos


def homogenize(vector: np.array) -> np.array:
    """Convert a vector from cartesian coordinates into homogeneous coordinates.

    Parameters
    ----------
    vector : np.array
        The vector to be converted.

    Returns
    -------
    homogeneous_vector : np.array
        The vector in homogeneous coordinates.


    Examples
    --------

    >>> import ropy.transform as rtf
    >>> import numpy as np
    >>> cartesian_vector = np.array((1, 2, 3))
    >>> rtf.homogenize(cartesian_vector)
    array([1., 2., 3., 1.])

    """
    vector = np.asarray(vector)

    shape = vector.shape
    homogeneous_vector = np.ones((*shape[:-1], shape[-1] + 1))
    homogeneous_vector[..., :-1] = vector
    return homogeneous_vector


def cartesianize(vector: np.array) -> np.array:
    """Convert a vector from homogeneous coordinates to cartesian coordinates.

    Parameters
    ----------
    vector : np.array
        The vector in homogeneous coordinates.

    Returns
    -------
    cartesian_vector : np.array
        The vector to be converted.

    Examples
    --------

    >>> import numpy as np
    >>> import ropy.transform as rtf
    >>> rtf.cartesianize(np.array((1, 2, 3, 41)))
    array([1., 2., 3.])
    >>> rtf.cartesianize((2, 0, 2, 2))
    array([1., 0., 1.])
    >>> rtf.cartesianize((2, 0, 2, 1))
    array([2., 0., 2.])
    >>> rtf.cartesianize((2, 0, 2, 2*np.sqrt(2)))
    array([0.70710678, 0.        , 0.70710678])
    >>> np.array((2, 0, 2)) / np.linalg.norm(np.array(( 2, 0, 2)))
    array([0.70710678, 0.        , 0.70710678])

    """
    vector = np.asarray(vector)

    return vector[..., :-1] / vector[..., -1]


def normalize_scale(vector: np.array) -> np.array:
    """Return an equivalent homogeneous vector with scale set to 1.

    Parameters
    ----------
    vector : np.array
        The vector (in homogeneous coordinates) to be scale-normalized.

    Returns
    -------
    vector : np.array
        An equivalent vector with scale component set to 1.

    Examples
    --------

    >>> import numpy as np
    >>> import ropy.transform as rtf
    >>> cartesian = np.array((1, 2, 3))
    >>> length = np.linalg.norm(cartesian)
    >>> length
    3.7416573867739413
    >>> cartesian / length
    array([0.26726124, 0.53452248, 0.80178373])
    >>> rtf.base.normalize_scale((*cartesian, length))
    array([0.26726124, 0.53452248, 0.80178373, 1.        ])

    """

    vector = np.asarray(vector)

    return vector / vector[-1]


def rotation_matrix(angle: float, u: np.array, v: np.array) -> np.array:
    """Return a rotation matrix to rotate by angle in the plane span by u and v.

    The function creates a N-dimensional rotation matrix that rotates a point by
    a set angle inside an oriented plane. The plane is defined by the two basis
    vectors u and v and the (positive) direction of rotation is from u to v.

    For example, if ``u=(1,0,0,1)`` (the x-axis) and ``v=(0,1,0,1)`` (the
    y-axis) then the resulting matrix rotates vectors counter-clockwise around
    the z-axis, i.e., it rotates vectors in the x-y plane.

    Parameters
    ----------
    angle : float
        The amount (in radians) by which to rotate the plane.
    u : np.array
        The first basis vectors (u,v) spanning the plane of
        rotation. The vector is given in homogeneous coordinates.
    v : np.array
        The second basis vectors (u,v) that span the plane of rotation. The
        vector is given in homogeneous coordinates.

    Returns
    -------
    rotation_matrix : np.array
        A matrix representing the rotation in homogeneous coordinates.

    Notes
    -----
    If u and v are not orthonormal, the resulting matrix is no longer a pure
    rotation.

    Examples
    --------


    """

    # This implementation is based on a very insightful stackoverflow
    # comment
    # https://math.stackexchange.com/questions/197772/generalized-rotation-matrix-in-n-dimensional-space-around-n-2-unit-vector#comment453048_197778

    u = cartesianize(np.asarray(u))
    v = cartesianize(np.asarray(v))

    ndim = u.size

    rotation_matrix = np.eye(ndim)
    rotation_matrix += sin(angle) * (np.outer(v, u) - np.outer(u, v))
    rotation_matrix += (cos(angle) - 1) * (np.outer(u, u) + np.outer(v, v))

    homogeneous_rotation = np.eye(ndim+1)
    homogeneous_rotation[:-1,:-1] = rotation_matrix

    return homogeneous_rotation


# other candidates for base functions:
# https://www.javatpoint.com/computer-graphics-homogeneous-coordinates
# (mainly for my own reference)
