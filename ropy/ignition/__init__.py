"""
:mod:`ropy.ignition`
====================

To use ``ropy.ignition``, you have to install the latest version of
Ignition_. In addition, you have to install
additional dependencies via

.. code-block:: bash

    pip install -e .[ignition]

-------

A collection of functions to ease interfacing with the Ignition software stack.
Ignition is a collection of libraries that, when combined, produce a general
purpose simulator for robotic applications called Ignition Gazebo. Ignition
Gazebo superseeds Gazebo and, among many other improvements, it is written as a
simulation library instead of being a stand-alone application. This allows for
dynamic control of all aspects of the simulation as well as full introspection.

Note that this module does not contain python bindings for ignition (and it does
not aim to do so). If you are looking for bindings check out
ScenarIO_,
which is a part of gym-ignition_.

.. autoclass:: ropy.ignition.Subscriber
    :members:
    :special-members: __init__

.. _gym-ignition: https://github.com/robotology/gym-ignition
.. _ScenarIO: https://robotology.github.io/gym-ignition/master/motivations/why_gym_ignition.html
.. _Ignition: https://ignitionrobotics.org/home
"""

from . import msgs as messages
from .subscriber import Subscriber
