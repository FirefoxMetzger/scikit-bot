"""
NumPy functions currently missing in Numba
"""

import numpy as np
from numba.extending import overload, register_jitable
from numba.np.unsafe.ndarray import to_fixed_tuple
from numba import types
from numpy.typing import ArrayLike


@overload(np.moveaxis)
def moveaxis(a: np.ndarray, source, destination) -> np.ndarray:
    """Move axes of an array to new positions.

    Other axes remain in their original order.

    Parameters
    ----------
    a : np.ndarray
        The array whose axes should be reordered.
    source : int or sequence of int
        Original positions of the axes to move. These must be unique.
    dest : int or sequence of int
        Destination positions for each of the original axes. These must also be unique.

    Returns
    -------
    result : np.ndarray
        Array with moved axes. This array is a view of the input array.

    Notes
    -----
    If one of (source, destination) is an integer, then the other must be an integer, too.

    See Also
    --------
    `np.moveaxis <https://numpy.org/doc/stable/reference/generated/numpy.moveaxis.html>`_
    """

    @register_jitable
    def impl_array(a: np.ndarray, source, destination):
        source_work = np.atleast_1d(np.asarray(source))
        destination_work = np.atleast_1d(np.asarray(destination))

        if source_work.size != destination_work.size:
            raise ValueError(
                "`source` and `destination` arguments must have "
                "the same number of elements"
            )

        for idx in range(source_work.size):
            if abs(source_work[idx]) > a.ndim:
                raise ValueError("Invalid axis in `source`.")
            if abs(destination_work[idx]) > a.ndim:
                raise ValueError("Invalid axis in `destination`.")

        source_work = [x % a.ndim for x in source_work]
        destination_work = [x % a.ndim for x in destination_work]

        order = [n for n in range(a.ndim) if n not in source_work]
        for dest, src in sorted(zip(destination_work, source_work)):
            order.insert(dest, src)

        oder_tuple = to_fixed_tuple(np.array(order), a.ndim)
        return np.transpose(a, oder_tuple)

    @register_jitable
    def impl_int(a: np.ndarray, source, destination):
        if abs(source) > a.ndim:
            raise ValueError("Invalid axis in `source`.")
        if abs(destination) > a.ndim:
            raise ValueError("Invalid axis in `destination`.")

        source = source % a.ndim
        destination = destination % a.ndim

        order = [n for n in range(a.ndim) if n != source]
        order.insert(destination, source)

        oder_tuple = to_fixed_tuple(np.array(order), a.ndim)
        return np.transpose(a, oder_tuple)

    if isinstance(source, types.Integer) and isinstance(destination, types.Integer):
        return impl_int
    else:
        return impl_array


@overload(np.putmask)
def putmask(a: np.ndarray, mask: ArrayLike, values: ArrayLike) -> None:
    """Changes elements of an array based on conditional and input values.

    Sets ``a.flat[n] = values[n]`` for each n where ``mask.flat[n]==True``.

    If `values` is not the same size as `a` and `mask` then it will repeat.
    This gives behavior different from ``a[mask] = values``.

    Parameters
    ----------
    a : ndarray
        Target array.
    mask : array_like
        Boolean mask array. It has to be the same shape as `a`.
    values : array_like
        Values to put into `a` where `mask` is True. If `values` is smaller
        than `a` it will be repeated.

    See Also
    --------
    np.place, np.put, np.take, np.copyto

    Examples
    --------
    >>> x = np.arange(6).reshape(2, 3)
    >>> np.putmask(x, x>2, x**2)
    >>> x
    array([[ 0,  1,  2],
           [ 9, 16, 25]])
    If `values` is smaller than `a` it is repeated:
    >>> x = np.arange(5)
    >>> np.putmask(x, x>1, [-33, -44])
    >>> x
    array([  0,   1, -33, -44, -33])
    """

    def impl(a: np.ndarray, mask: ArrayLike, values: ArrayLike) -> None:
        mask = np.asarray(mask)
        values = np.atleast_1d(np.asarray(values))

        for idx in range(a.size):
            if mask.flat[idx]:
                a.flat[idx] = values.flat[idx % len(values)]

    return impl
