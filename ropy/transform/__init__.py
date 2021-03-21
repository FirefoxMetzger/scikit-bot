"""
``ropy.transform``
==================

A collection of functions to help converting between different coordinate
systems using homogeneous transformations.

The functions in this library expect homogeneous coordinates (as opposed to
cartesian coordinates). You can transform a vector between to homogeneous
corrdinates using ``transform.homogenize``, and you can transform a vector back
to cartesian coordinages using ``transform.cartesianize``.

Coordinates
-----------

Functions to transform between coordinate systems. 


Projections
-----------

Functions to compute perspective transformations

"""

from .base import homogenize, cartesianize, normalize_scale

from . import (base, coordinates, projections)