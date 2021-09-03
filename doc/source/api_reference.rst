.. _api-reference:

API Reference
=============

Scikt-bot is structured into a set of independent modules which you can import via

.. autosummary::
    :toctree: _autosummary

    skbot.ignition
    skbot.inverse_kinematics
    skbot.ros
    skbot.trajectory
    skbot.transform

Some modules have additional dependencies on top of the scipy stack. To
use these modules you will have to install scikit-bot with the respective extra
requirements, e.g. you will have to use

.. code-block:: bash

    pip install -e .[ignition]

to use :mod:`skbot.ignition`. Whenever a module has additional requirements it will state
these in it's module-level documentation.

.. _Ignitionrobotics: https://ignitionrobotics.org/
