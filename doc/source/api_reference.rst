API Reference
=============


Ropy is structured into a set of independent modules which you can import via
``ropy.<modulename>``.

.. contents:: Available Modules
    :depth: 2

Some modules have additional dependencies on top of the basic scipy stack. To
use these modules you will have to install ropy with the respective extra
targets, e.g. you will have to use

.. code-block:: bash

    pip install -e .[ignition]

to use ``ropy.ignition``. Whenever a module has additional requirements it will state
these in it's module-level documentation.

.. automodule:: ropy.transform
.. automodule:: ropy.ignition