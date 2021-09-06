import numpy as np
from numpy.typing import ArrayLike
from numba.extending import register_jitable, overload
from numba.np.unsafe.ndarray import to_fixed_tuple
import numba


def reduce(
    reduce_op, x: np.ndarray, axis: ArrayLike, keepdims: bool = False
) -> np.ndarray:
    return NotImplementedError("This function is Numba only.")


@overload(reduce)
def numba_reduce(reduce_op, x, axis, keepdims=False) -> np.ndarray:
    """Reduce an array along the given axes.

    Parameters
    ----------
    reduce_op
        The reduce operation to call for each element of the output array. The input to
        reduce_op is a flattened, contigous array representing the window upon which
        reduce_op operates. It returns a scalar.
    x : np.ndarray
        The array to reduce.
    axis : ArrayLike
        The axis along which to reduce. This can be multiple axes.
    keepdims : bool
        If ``True``, keep the dimensions along which the array was reduced. If ``False``
        squeeze the output array. Currently only ``True`` is supported.

    Returns
    -------
    out_array : np.ndarray
        The reduced array.

    """

    @register_jitable
    def impl_keepdims(reduce_op, x, axis, keepdims=False):
        axis = np.atleast_1d(np.asarray(axis))

        mask = np.zeros(x.ndim, dtype=np.bool8)
        mask[axis] = True

        original_shape = np.array(x.shape)
        squeezed_shape = original_shape[~mask]

        # this could be reversed, but we are calling a reduction op on it anyway
        new_axes = -np.arange(1, axis.size + 1)

        # not that this will copy if reduction happens along a non-contigous axis
        x_work = np.moveaxis(x, axis, new_axes)
        x_work = np.ascontiguousarray(x_work)

        total_reduce = np.prod(original_shape[axis])
        total_keep = np.prod(squeezed_shape)
        tmp_shape = to_fixed_tuple(np.array((total_keep, total_reduce)), 2)
        x_work = np.reshape(x_work, tmp_shape)

        result = np.empty((total_keep,), dtype=x_work.dtype)
        for idx in range(result.size):
            result[idx] = reduce_op(x_work[idx, ...])

        new_shape = original_shape.copy()
        new_shape[axis] = 1
        new_shape_tuple = to_fixed_tuple(new_shape, x.ndim)
        return np.reshape(result, new_shape_tuple)

    @register_jitable
    def impl_dropdims(reduce_op, x, axis, keepdims=False):
        axis = np.atleast_1d(np.asarray(axis))

        if axis.size > 1:
            raise NotImplementedError("Numba can't np.squeeze yet.")

        result = impl_keepdims(reduce_op, x, axis)
        result = np.moveaxis(result, axis, 0)

        return result[0, ...]

    if isinstance(keepdims, numba.types.Literal):
        should_keep = keepdims.literal_value
    elif isinstance(keepdims, bool):
        should_keep = keepdims
    # elif isinstance(keepdims, numba.types.boolean):
    #     should_keep = False
    else:
        raise NotImplementedError(f"Unsupported type for `keepdims`: {type(keepdims)}")

    if should_keep:
        return impl_keepdims
    else:
        return impl_dropdims


@numba.jit(nopython=True, cache=True)
def vector_project(a: ArrayLike, b: ArrayLike, axis: int = -1) -> np.ndarray:
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

    numerator = reduce(np.sum, a * b, axis=axis, keepdims=True)
    denominator = reduce(np.sum, b * b, axis=axis, keepdims=True)

    return numerator / denominator * b


@numba.jit(nopython=True, cache=True)
def scalar_project(
    a: ArrayLike, b: ArrayLike, axis: int = -1, keepdims=False
) -> np.ndarray:
    """Returns the length of the components of each a along each b."""

    a = np.asarray(a)
    b = np.asarray(b)

    projected = vector_project(a, b, axis=axis)
    magnitude = reduce(np.linalg.norm, projected, axis=axis, keepdims=keepdims)
    sign = np.sign(reduce(np.sum, projected * b, axis=axis, keepdims=keepdims))

    return sign * magnitude


@numba.jit(nopython=True, cache=True)
def angle_between(
    vec_a: ArrayLike, vec_b: ArrayLike, axis: int = -1, eps=1e-10
) -> np.ndarray:
    """Computes the angle from a to b (in a right-handed frame)

    Notes
    -----
    Implementation is based on this StackOverflow post:
    https://scicomp.stackexchange.com/a/27694
    """

    vec_a = np.expand_dims(np.asfarray(vec_a), 0)
    vec_b = np.expand_dims(np.asfarray(vec_b), 0)

    if axis >= 0:
        axis += 1

    len_c = reduce(np.linalg.norm, vec_a - vec_b, axis=axis)
    len_a = reduce(np.linalg.norm, vec_a, axis=axis)
    len_b = reduce(np.linalg.norm, vec_b, axis=axis)

    mask = len_a >= len_b
    tmp = np.where(mask, len_a, len_b)
    np.putmask(len_b, ~mask, len_a)
    len_a = tmp

    mask = len_c > len_b
    mu = np.where(mask, len_b - (len_a - len_c), len_c - (len_a - len_b))

    numerator = ((len_a - len_b) + len_c) * mu
    denominator = (len_a + (len_b + len_c)) * ((len_a - len_c) + len_b)

    mask = denominator > eps
    angle = np.divide(numerator, denominator)  # , where=mask)
    angle = np.sqrt(angle)
    angle = np.arctan(angle)
    angle *= 2
    np.putmask(angle, ~mask, np.pi)
    return angle[0]
