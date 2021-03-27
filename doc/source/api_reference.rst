.. _api-reference:

API Reference
=============

Ropy is structured into a set of independent modules which you can import via

- :mod:`ropy.transform` Coordinate transformations and projections.
- :mod:`ropy.trajectory` Interpolation of parameterized curves.
- :mod:`ropy.ignition` Interface with Ignitionrobotics_ libraries.

Some modules have additional dependencies on top of the scipy stack. To
use these modules you will have to install ropy with the respective extra
requirements, e.g. you will have to use

.. code-block:: bash

    pip install -e .[ignition]

to use ``ropy.ignition``. Whenever a module has additional requirements it will state
these in it's module-level documentation.

.. automodule:: ropy.transform
    :members:
.. automodule:: ropy.trajectory
.. automodule:: ropy.ignition

.. _Ignitionrobotics: https://ignitionrobotics.org/
