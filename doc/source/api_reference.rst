.. _api-reference:
API Reference
=============

Ropy is structured into a set of independent modules which you can import via

- :mod:`ropy.transform`
- :mod:`ropy.ignition`

Some modules have additional dependencies on top of the scipy stack. To
use these modules you will have to install ropy with the respective extra
requirements, e.g. you will have to use

.. code-block:: bash

    pip install -e .[ignition]

to use ``ropy.ignition``. Whenever a module has additional requirements it will state
these in it's module-level documentation.

.. automodule:: ropy.transform
.. automodule:: ropy.ignition