import numpy as np
from math import sin, cos
from numpy.core.records import array
from numpy.typing import ArrayLike


def homogenize(vector: ArrayLike) -> np.ndarray:
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


def cartesianize(vector: ArrayLike) -> np.ndarray:
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


def normalize_scale(vector: ArrayLike) -> np.ndarray:
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


def rotation_matrix(angle: float, u: ArrayLike, v: ArrayLike) -> np.ndarray:
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
    .. plot::
        :include-source:

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> import ropy.transform as rtf
        >>> rotation = rtf.base.rotation_matrix(np.pi/4, (1, 0, 1), (0, 1, 1))
        >>> points = rtf.homogenize(np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]]))
        >>> points_rotated = np.matmul(rotation, points.T)
        >>> fig, ax = plt.subplots()
        >>> ax.plot(points[:, 0], points[:, 1], points_rotated[0], points_rotated[1])
        >>> ax.legend(["Original", "Rotated 45°"])
        >>> fig.show()

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

    homogeneous_rotation = np.eye(ndim + 1)
    homogeneous_rotation[:-1, :-1] = rotation_matrix

    return homogeneous_rotation


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
    rotated_vector : np.array
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
    sheared : np.Array
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
