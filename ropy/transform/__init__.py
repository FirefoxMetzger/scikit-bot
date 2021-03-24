"""
:mod:`ropy.transform`
=====================

A collection of functions to help converting between different cartesian
coordinate systems via homogeneous transformations.

The functions in this library expect homogeneous coordinates (as opposed to
cartesian coordinates). You can transform a vector between to homogeneous
corrdinates using ``transform.homogenize``, and you can transform a vector back
to cartesian coordinages using ``transform.cartesianize``.

.. autofunction:: ropy.transform.homogenize 
.. autofunction:: ropy.transform.cartesianize

.. automodule:: ropy.transform.base
    :members:

.. automodule:: ropy.transform.coordinates
    :members:

.. automodule:: ropy.transform.projections 
    :members:

"""

from .base import _homogenize as homogenize
from .base import _cartesianize as cartesianize

from . import base, coordinates, projections

__all__ = ["homogenize", "cartesianize", "base", "coordinates", "projections"]
