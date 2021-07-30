"""
Interface with Ignitionrobotics_ libraries.


.. note::

    To use :mod:`ropy.ignition`, you have to install the latest version of
    Ignition_. In addition, you have to install
    additional dependencies via

    .. code-block:: bash

        pip install -e .[ignition]

:mod:`ropy.ignition` is a collection of functions to ease interfacing with the
Ignition software stack. Ignition is a collection of libraries that, when
combined, produce a general purpose simulator for robotic applications called
Ignition Gazebo. Ignition Gazebo superseeds Gazebo and, among many other
improvements, it is written as a simulation library instead of being a
stand-alone application. This allows for dynamic control of all aspects of the
simulation as well as full introspection.

Note that this module does not contain python bindings for ignition (and it does
not aim to do so). If you are looking for bindings check out
ScenarIO_,
which is a part of gym-ignition_.


Functions
---------

.. autosummary::
    :toctree:

    ropy.ignition.Subscriber
    ropy.ignition.FrustumProjection
    ropy.ignition.create_frame_graph


Messages
--------

Ropy provides python bindings to all Ignition messages. Messages are build
from the protocol buffer templates found in Ign-Msgs_. This allows you to decode
messages sent by the subscriber.

To build the bindings yourself, run

.. code-block:: bash

    git clone https://github.com/ignitionrobotics/ign-msgs.git
    mkdir ign-bindings
    protoc -I ign-msgs/proto/ --python_betterproto_out=ign-bindings ign-msgs/proto/ignition/msgs/*

This will produce a file called `ignition/msgs.py` in the chosen output location
which can be used to decode messages.

Members of ``ropy.ignition.messages`` are not documented here (the class is
fully auto-generated). Instead, an overview can be found in the `Ignition
documentation`_.

.. _gym-ignition: https://github.com/robotology/gym-ignition
.. _ScenarIO: https://robotology.github.io/gym-ignition/master/motivations/why_gym_ignition.html
.. _Ignition: https://ignitionrobotics.org/home
.. _`Ign-Msgs`: https://github.com/ignitionrobotics/ign-msgs
.. _`Ignition documentation`: https://ignitionrobotics.org/api/msgs/6.4/index.html
.. _Ignitionrobotics: https://ignitionrobotics.org/
"""

from . import messages
from .subscriber import Subscriber
from .transformations import FrustumProjection
from .sdformat.create_frame_graph import create_frame_graph
from . import sdformat

__all__ = [
    "messages",
    "Subscriber",
    "FrustumProjection",
    "create_frame_graph",
    "sdformat",
]
