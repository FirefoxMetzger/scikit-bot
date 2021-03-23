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
following the official instructions::

    https://ignitionrobotics.org/docs/dome

Then you can install ``ropy`` with additional dependencies

.. code-block:: bash

    git clone https://github.com/FirefoxMetzger/ropy.git
    cd ropy
    pip install -e .[ignition]


Building the Docs locally
-------------------------

.. code-block:: bash

    git clone https://github.com/FirefoxMetzger/ropy.git
    cd ropy
    pip install -e .[docs]
    sphinx-build -b html doc/source doc/build

.. _Ignition: https://ignitionrobotics.org/home
