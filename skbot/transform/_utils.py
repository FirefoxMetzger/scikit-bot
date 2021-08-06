import numpy as np
from numpy.typing import ArrayLike


def vector_project(a: ArrayLike, b: ArrayLike, *, axis: int = -1) -> np.ndarray:
    """Returns the components of each a along each b.

    Parameters
    ----------
    a : ArrayLike
        A batch of vectors to be projected.
    b : ArrayLike
        A batch of vectors that are being projected onto.
    axis : int
        The data axis of the batches, i.e., along which axis to compute.

    Returns
    -------
    result : ndarray
        A batch of vectors of shape [a.batch_dims, b.batch_dims].


    Notes
    -----
    The function assumes that a and b are broadcastable.

    """

    a = np.asarray(a)
    b = np.asarray(b)

    numerator = np.sum(a * b, axis=axis, keepdims=True)
    denominator = np.sum(b * b, axis=axis, keepdims=True)

    return numerator / denominator * b


def scalar_project(
    a: ArrayLike, b: ArrayLike, *, axis: int = -1, keepdims=False
) -> np.ndarray:
    """Returns the length of the components of each a along each b."""

    projected = vector_project(a, b, axis=axis)
    magnitude = np.linalg.norm(projected, axis=axis, keepdims=keepdims)
    sign = np.sign(np.sum(projected * b, axis=axis, keepdims=keepdims))

    return sign * magnitude


def angle_between(vec_a: ArrayLike, vec_b: ArrayLike, *, axis: int = -1) -> np.ndarray:
    """Computes the angle from a to b (in a right-handed frame)

    Notes
    -----
    Implementation is based on this StackOverflow post:
    https://scicomp.stackexchange.com/a/27694
    """

    vec_a = np.asarray(vec_a)[None, :]
    vec_b = np.asarray(vec_b)[None, :]

    if axis >= 0:
        axis += 1

    len_c = np.linalg.norm(vec_a - vec_b, axis=axis)
    len_a = np.linalg.norm(vec_a, axis=axis)
    len_b = np.linalg.norm(vec_b, axis=axis)

    mask = len_a >= len_b
    tmp = np.where(mask, len_a, len_b)
    np.putmask(len_b, ~mask, len_a)
    len_a = tmp

    mask = len_c > len_b
    mu = np.where(mask, len_b - (len_a - len_c), len_c - (len_a - len_b))

    numerator = ((len_a - len_b) + len_c) * mu
    denominator = (len_a + (len_b + len_c)) * ((len_a - len_c) + len_b)

    mask = denominator != 0
    angle = np.divide(numerator, denominator, where=mask)
    np.sqrt(angle, out=angle)
    np.arctan(angle, out=angle)
    angle *= 2
    np.putmask(angle, ~mask, np.pi)
    return angle[0]


# def rotation_direction(vec_a: ArrayLike, vec_b: ArrayLike, *, axis=-1):
#     vec_a = np.asarray(vec_a)[None, :]
#     vec_b = np.asarray(vec_b)[None, :]

#     vec_a = np.moveaxis(vec_a, axis, -1)
#     vec_b = np.moveaxis(vec_b, axis, -1)

#     joint_shape = np.broadcast_shapes(vec_a.shape, vec_b.shape)
#     vec_a = np.broadcast_to(vec_a, joint_shape)
#     vec_b = np.broadcast_to(vec_b, joint_shape)

#     rotation_projection = np.stack((vec_a, vec_b), axis=-2)
#     u, _, v = np.linalg.svd(rotation_projection)
#     directions = np.sign(np.linalg.det(u)*np.linalg.det(v))

#     directions = np.moveaxis(directions, -1, axis)

#     return directions
