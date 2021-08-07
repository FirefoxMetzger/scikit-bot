Installation
============

Basic Installation
------------------

.. code-block:: bash

    pip install scikit-bot

Install with Ignition Support
-----------------------------

To use scikit-bot together with Ignition_, you first have to install Ignition
following the `official instruction`_. Then you can install
scikit-bot with additional dependencies

.. code-block:: bash

    pip install scikit-bot[ignition]

**Note**: This also works incrementally, meaning that you can do this on
top of an existing scikit-bot installation.

Development Installation
------------------------

This installation sets up an editable installation with docs, linting, and
testing dependencies. If you want to develop modules that have additional
depdencies, you need to install these dependencies on top of this installation.
If you encounter difficulties during the setup, feel free to create a `new issue`_.

.. code-block:: bash

    git clone https://github.com/FirefoxMetzger/ropy.git
    cd ropy
    pip install -e .[docs,linting,testing]

Before you submit a PR make sure all tests pass, that all code is covered by tests,
that you follow our code-style conventions, and that the documentation builds without
errors. Here is how to perform each task (in the projects root directory).

- Run all tests: ``pytest``
- Coverage: ``coverage run -m pytest .`` followed by ``coverage report``
- Code-Style: ``black .``
- Docs: ``sphinx-build -b html doc/source doc/build``


.. _Ignition: https://ignitionrobotics.org/home
.. _`official instruction`: https://ignitionrobotics.org/docs/dome
.. _`new issue`: https://github.com/FirefoxMetzger/ropy/issues