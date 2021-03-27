Ropy Documentation
===================

You have found to the ``ropy`` documentation. You can find API documentation and
examples here.

.. toctree::
   :maxdepth: 1

   install
   examples
   api_reference

Ropy is a robotics library that aims to address the large heterogeneity of code
in the robotics community by providing a selection of commonly used algorithms
and functions in an easy access manner. It focusses on begin easy to use and on
enabling rapid prototyping.

Ropy includes functions for coordinate transformations and projections,
functions for trajectory generation and kinematics, and many more, yet, it is
not a simulator or robotics framework. It is a library meant to complement
existing tools. With ropy, you can quickly try things in python first, get it
working, and then integrate it into your framework of choice; potentially, using
one of our existing modules to interface with the framework, saving you more
time.

Ropy is heavily inspired by the scipy stack (numpy, scikit-learn, matplotlib,
...) and leans heavily on it. This means seamless interoparability with the
scipy stack, but also allows for easy integration with current machine learning
libraries such as pytorch or tensorflow.

Ropy follows a python-first approach. Typically, robotics frameworks are written
in plain C or C++ and, if it is possible to use via python, support is
rudementary at best. In Ropy, python is a first-class citizen with the majority
of the code being written in plain python. The rationale is that the majority of
work done in robotics is prototyping, and prototyping is much (much) faster in
an interpreted language than a compiled one. It is significantly more efficient
to write code that works first (leveraging pythons amazing debugging
capabilities) and then optimize for speed, than it is to debug broken, fast
code.

Curious? Check out our detailed :ref:`API documentation<api-reference>` to see
if there is anything that meets your need. Got an idea for a new feature or
spotted something that is missing? Submit a `feature request`_.

.. _`feature request`: https://github.com/FirefoxMetzger/ropy/issues
