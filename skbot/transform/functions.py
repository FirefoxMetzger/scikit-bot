import numpy as np
from numpy.typing import ArrayLike

from .base import Frame
from ._utils import vector_project


def scale(vector: ArrayLike, scalar: ArrayLike) -> np.ndarray:
    """Scale each dimension of a vector.

    Multiplies each dimension of ``vector`` with the matching dimension of
    ``scalar``. If necessary, ``scalar`` will be broadcasted.

    Parameters
    ----------
    vector : ArrayLike
        A vector to be scaled.
    scalar : ArrayLike
        A vector representing the amount by which to scale each dimension.

    Returns
    -------
    scaled : ArrayLike
        A vector where each dimension is scaled by scalar.

    Notes
    -----
    Exists for completeness. It may be cleaner to simply write
    ``scalar * vector`` instead.

    """
    vector = np.asarray(vector)
    scalar = np.asarray(scalar)

    return scalar * vector


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


def rotate(vector: ArrayLike, u: ArrayLike, v: ArrayLike, *, axis=-1) -> np.ndarray:
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
    axis : int
        The axis along which to compute the reflection. Default: -1.

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
    return reflect(reflect(vector, u, axis=axis), v, axis=axis)


def reflect(vector: ArrayLike, direction: ArrayLike, *, axis=-1) -> np.ndarray:
    """Reflect a vector along a line defined by direction.

    Parameters
    ----------
    vector : ArrayLike
        The vector to be reflected.
    direction : ArrayLike
        The vector describing the direction along which the reflection takes place.
    axis : int
        The axis along which to compute the reflection. Default: -1.

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

    return vector - 2 * vector_project(vector, direction, axis=axis)


def shear(
    vector: ArrayLike, direction: ArrayLike, amount: ArrayLike, *, axis=-1
) -> np.ndarray:
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
    axis : int
        The axis along with to compute the shear.

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

    tmp1 = np.sum(vector * amount, axis=axis)

    return vector + tmp1 * direction


def as_affine_matrix(from_frame: Frame, to_frame: Frame, *, axis: int = -1):
    """Transformation Matrix between two frames at a given point.

    Given two frames ``from_frame`` and ``to_frame`` that represent affine space
    and are connected by a sequence of linear transformations, compute a matrix
    representation of the transformation.

    Parameters
    ----------
    from_frame : tf.Frame
        The parent frame.
    to_frame : tf.Frame
        The child frame.
    axis : int
        The axis along which computation takes place. All other axes are considered
        batch dimensions.

    Returns
    -------
    matrix : np.ndarray
        The matrix representation of the transformation. It will have the shape
        ``(batch_shape, to_frame.ndim, from_frame.ndim)``.

    Notes
    -----
    The matrix representation will only be accurate if the transformation chain
    between the two given frames is linear.

    The

    """

    if axis != -1:
        raise NotImplementedError("Axis is not implemented yet.")

    basis_set = np.eye(from_frame.ndim)
    basis_set[:, -1] = 1

    mapped_basis = from_frame.transform(basis_set, to_frame).T

    # normalize affine matrix
    scaling = mapped_basis[-1, :]
    mapped_basis /= scaling[None, :]
    mapped_basis[..., :-1] -= mapped_basis[..., -1][..., None]

    return mapped_basis
