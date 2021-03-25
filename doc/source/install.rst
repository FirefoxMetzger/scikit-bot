Installation
============

Basic Installation
------------------

.. code-block:: bash

    git clone https://github.com/FirefoxMetzger/ropy.git
    cd ropy
    pip install -e .

Install with Ignition Support
-----------------------------

To use ``ropy`` together with Ignition_, you first have to install Ignition
following the `official instruction`_. Then you can install
``ropy`` with additional dependencies

.. code-block:: bash

    git clone https://github.com/FirefoxMetzger/ropy.git
    cd ropy
    pip install -e .[ignition]

**Note**: This also works incrementally, meaning that you can do this on
top of an existing ropy installation.

Building the Docs locally
-------------------------

.. code-block:: bash

    git clone https://github.com/FirefoxMetzger/ropy.git
    cd ropy
    pip install -e .[docs]
    sphinx-build -b html doc/source doc/build

.. _Ignition: https://ignitionrobotics.org/home
.. _`official instruction`: https://ignitionrobotics.org/docs/dome
