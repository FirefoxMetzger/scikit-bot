"""
Interface with Ignitionrobotics_ libraries.


.. note::

    To use :mod:`skbot.ignition`, you have to install the latest version of
    Ignition_. In addition, you have to install
    additional dependencies via

    .. code-block:: bash

        pip install -e .[ignition]

:mod:`skbot.ignition` is a collection of functions to ease interfacing with the
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


.. currentmodule:: skbot.ignition

Functions
---------

.. rubric:: General

.. autosummary::
    :toctree:

    skbot.ignition.create_frame_graph
    skbot.ignition.download_fuel_model
    skbot.ignition.FrustumProjection
    skbot.ignition.get_fuel_model
    skbot.ignition.get_fuel_model_info
    skbot.ignition.Subscriber

.. rubric:: SDFormat Specific

.. note::
    Scikit-bot will automatically select the correct version when using
    :func:`skbot.ignition.sdformat.loads`; however, it is imporant that you are
    mindful of the version you are using, since SDFormat doesn't use SemVer and
    availability of elements may differ slightly across versions.

.. autosummary::
    :toctree:

    skbot.ignition.sdformat.dumps
    skbot.ignition.sdformat.get_version
    skbot.ignition.sdformat.loads
    skbot.ignition.sdformat.loads_generic
    skbot.ignition.sdformat.to_frame_graph


SDFormat XML
------------

.. note::
    You can find more documentation aboud SDFormat in the `official spec <http://sdformat.org/spec>`_.

.. rubric:: _`XSD Schema Files`

.. warning::
    The XSD bindings are (slightly) oppinionated and promote some optional
    elements to required elements with a default value. Check the content of
    this section for details.

Scikit-bot comes with XSD1.1 schema files that describe SDFormat. You can find their
latest versions inside the skbot/ignition/sdformat folder. You can view them on
GitHub and a copy can be found in your local version, too. Contrary to the
official SDFormat, schemas are provided for *all* SDF versions.

The XSD bindings are (slightly) oppinionated. If a SDF element is optional (the
spec denotes this as required=0 or required=*) but specifies a default value,
the schema promotes this to a *required* element with a default value. This is
done to allow the python bindings to provide you with auto-populated defaults
where possible.

.. rubric:: _`SDF Bindings`

Scikit-bot features a DOM-style parser and serializer for SDFormat XML. You can load
all SDFormat versions and scikit-bot will construct a class tree out of it.
Similarily, you can construct objects that represent SDF elements and scikit-bot can
serialize them into SDF. 

The API used here mimics the API used by the familiar `JSON parser <json>`_ or
`YAML parser <yaml>`_. The main difference is that this module returns an object
tree of dataclass objects, whilst JSON and YAML return dictionaries.

While the parser is imported together with :mod:`skbot.ignition`, the individual
models are imported on demand. This is done to keep import times low. To use the
bindings explicitly you must import them explicitly. Check the individual
bindings for documentation on how to do this:

.. autosummary::
    :template: sdformat_model.rst
    :toctree:
    :recursive:

    skbot.ignition.sdformat.bindings.v18
    skbot.ignition.sdformat.bindings.v17
    skbot.ignition.sdformat.bindings.v16
    skbot.ignition.sdformat.bindings.v15
    skbot.ignition.sdformat.bindings.v14
    skbot.ignition.sdformat.bindings.v13
    skbot.ignition.sdformat.bindings.v12
    skbot.ignition.sdformat.bindings.v10

Ignition Messages
-----------------

Scikit-bot provides python bindings to all Ignition messages. Messages are build
from the protocol buffer templates found in Ign-Msgs_. This allows you to decode
messages sent by the subscriber.

To build the bindings yourself, run

.. code-block:: bash

    git clone https://github.com/ignitionrobotics/ign-msgs.git
    mkdir ign-bindings
    protoc -I ign-msgs/proto/ --python_betterproto_out=ign-bindings ign-msgs/proto/ignition/msgs/*

This will produce a file called `ignition/msgs.py` in the chosen output location
which can be used to decode messages.

Members of ``skbot.ignition.messages`` are not documented here (the class is
fully auto-generated). Instead, an overview can be found in the `Ignition
documentation`_.

.. _gym-ignition: https://github.com/robotology/gym-ignition
.. _ScenarIO: https://robotology.github.io/gym-ignition/master/motivations/why_gym_ignition.html
.. _Ignition: https://ignitionrobotics.org/home
.. _`Ign-Msgs`: https://github.com/ignitionrobotics/ign-msgs
.. _`Ignition documentation`: https://ignitionrobotics.org/api/msgs/6.4/index.html
.. _Ignitionrobotics: https://ignitionrobotics.org/
.. _yaml: https://pyyaml.org/wiki/PyYAMLDocumentation
.. _json: https://docs.python.org/3/library/json.html
"""

from . import messages
from .subscriber import Subscriber
from .transformations import FrustumProjection
from .sdformat.create_frame_graph import create_frame_graph
from . import sdformat
from .fuel import get_fuel_model_info, download_fuel_model, get_fuel_model

__all__ = [
    "messages",
    "Subscriber",
    "FrustumProjection",
    "create_frame_graph",
    "sdformat",
    "get_fuel_model_info",
    "download_fuel_model",
    "get_fuel_model",
    "transform_graph_from_sdf",
]
