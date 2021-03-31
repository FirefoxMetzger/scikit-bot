"""
:mod:`ropy.transform`
=====================

A collection of functions to help converting between different cartesian
coordinate systems via homogeneous transformations.

The functions in this library expect homogeneous coordinates (as opposed to
cartesian coordinates). You can transform a vector between to homogeneous
corrdinates using ``transform.homogenize``, and you can transform a vector back
to cartesian coordinages using ``transform.cartesianize``.

"""

from .base import homogenize
from .base import cartesianize
from .base import normalize_scale
from .base import rotation_matrix

from .coordinates import transform, inverse_transform, transform_between

from .projections import perspective_frustum


__all__ = [
    "homogenize",
    "cartesianize",
    "transform",
    "inverse_transform",
    "transform_between",
    "perspective_frustum",
    "rotation_matrix"
]
