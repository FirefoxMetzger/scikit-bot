"""
:mod:`ropy.transform`
=====================

A collection of functions to help converting between different cartesian
coordinate systems via homogeneous transformations.

The functions in this library expect homogeneous coordinates (as opposed to
cartesian coordinates). You can transform a vector between to homogeneous
corrdinates using ``transform.homogenize``, and you can transform a vector back
to cartesian coordinages using ``transform.cartesianize``.

Space Conversion
----------------

Helper functions to convert vectors between cartesian and homogeneous vector
spaces.

.. autofunction:: ropy.transform.homogenize 
.. autofunction:: ropy.transform.cartesianize


Base
----

Basic functions used as building blocks by higher-level submodules.

.. automodule:: ropy.transform.base
    :members:

Coordinates
-----------

Functions to transform between coordinate systems. 


.. automodule:: ropy.transform.coordinates
    :members:


Projections
-----------

Functions to compute perspective transformations

.. automodule:: ropy.transform.projections 
    :members:

"""

from .base import _homogenize as homogenize
from .base import _cartesianize as cartesianize

from . import (base, coordinates, projections)