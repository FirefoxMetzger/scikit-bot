""" 

Reading and Writing SDFormat XML
================================

.. currentmodule:: skbot.ignition

Scikit-bot comes with bindings and schemata to read and write SDFormat. SDFormat
(Simulation Description Format) is a - pretty extensive - XML format that is
primarily intended to describe simulation worlds and robots. It was originially
developed for the `Gazebo simulator <http://gazebosim.org/>`_ (now superseeded by
`Ignition Gazebo <https://ignitionrobotics.org/home>`_) and is developed by
Ignition robotics. If you are unfamiliar with SDFormat, take a look at their
`official website <http://sdformat.org/>`_ and check the specification and
documentation.

The bindings provided by scikit-bot aim to help you write and modify SDFormat
files, and to allow python code to consume SDF files in a natural manner.
Examples for the former are (a) validation and verification of existing SDF, or
(b) procedual generation of SDF files for simulation. An example for the latter
is scikit-bot itself, which can build a frame graph from SDF, which - among
other things - gives you easy access to things like forward kinematics.

.. note::
    While this example is primarily concerned with reading/writing SDF in
    python, it is worthwhile to point out that scikit-bot ships with XSD1.1
    bindings for SDFormat. You can find them in your module folder or `here on
    GitHub
    <https://github.com/FirefoxMetzger/scikit-bot/tree/main/skbot/ignition/sdformat/schema>`_.

"""

# %%
# Importing the Bindings
# ----------------------
#

import skbot.ignition as ign
from skbot.ignition.sdformat.bindings import v18
from pathlib import Path
from dataclasses import dataclass, field
from typing import Tuple

# %%
# The SDFormat bindings are part of scikit-bot's :mod:`ignition module
# <skbot.ignition>`. The ignition module has additional dependencies, and
# - as such - you will have to install these as well. instructions on how to do
# this can be found in the :mod:`module's documentation <skbot.ignition>`.
#
# Another thing to note is that the SDFormat bindings are not imported together
# with the ignition module. This is a conscious choice, as the bindings for each
# versions are quite large. To keep import times low, the version-specific
# bindings are lazy-loaded whenever scikit-bot needs them or when you import
# them explicitly::
#
#    from skbot.ignition.sdformat.bindings import vXX
#
# where ``vXX``` is the version you wish to use. In this example we use ``v18``
# for SDFormat v1.8.
#
# Reading / Deserialization
# -------------------------
#
# .. note::
#    You don't have to explicitly import bindings to load SDF. The required
#    version will be lazy-loaded for you.
#
# Scikit-bot reads SDFormat from strings containing valid XML. While we might
# support directly reading from file in the future, pythons built-in ability to
# read files and manage the filesystem are very extensive and there is little
# you can't accomplish in one or two lines. You can find examples how to do this
# further down on this page.
#
# Let's start with a small SDF string.
#

sdf_string = """<?xml version="1.0" ?>
<sdf version="1.8">
  <model name="camera_model">
    <link name="camera_link">
        <pose>1 2 3 0 0 0</pose>
        <sensor name="camera_sensor" type="camera">
            <camera>
                <image></image>
            </camera>
        </sensor>
    </link>
  </model>
</sdf>
"""

# %%
# If you use the above SDF in Ignition Gazebo, it will place a basic perspective
# camera into your world at position (1, 2, 3) relative to the world's reference
# frame. There is, of course, much more to SDF and you can express entire robot
# kinematics, animated models, worlds for accurate phyics simulation, and much
# more. However, a tutorial on these is out of scope here, so please refer to
# the official docs for more information on that. Here, the above will serve as
# a nice example.
#
# To read / deserialize the above SDF simply feed it into skbot's SDF reader
#

sdf_root: v18.Sdf = ign.sdformat.loads(sdf_string)
# %%
# A few things have happened here. Scikit-bot took the string, looked at the
# version of the SDF inside it, and loaded the required data-bindings. It then
# used those bindings to parse the string and create a corresponding tree of
# python objects. It also populated all the missing/omitted fields with their
# default values where applicable. Finally, we used python type-hints to declare
# that ``sdf_root`` is a SDFormat v1.8 root tag. This gives us access
# to auto-completion within most modern IDEs and allows static type validation
# via `mypy <http://mypy-lang.org/>`_.

@dataclass
class Foo:
    bar:int

img_dims = (
    sdf_root.model.link[0].sensor[0].camera.image.height,
    sdf_root.model.link[0].sensor[0].camera.image.width,
)
print(f"The camera resolution is: {img_dims}")

Foo(sdf_root.model.link[0].sensor[0].camera.image.height)
#%%
# Auto-populated defaults is one of the advantages of using data-bindings
# compared to parsing with generic XML parsers like ``xml.etree`` or `lxml
# <https://lxml.de/>`_. Another advantage is implicit validation; if your
# SDF contains invalid elements, you will get an exception telling you
# what's off.

# TODO: example of ign.loads on invalid SDF

#%%
# :func:`sdformat.loads` comes with a few keyword arguments that are noteworthy.
# Sometimes you may wish to force loading SDF as a certain version that differs from
# the one reported in the file. You can do this by specifying the version to use.

v17_string = ign.sdformat.loads(sdf_string, version="1.7")

#%%
# You can also check the version of a given SDF without fully parsing it, which
# can be faster and also doesn't load any bindings.

ver = ign.sdformat.get_version(sdf_string)

#%%
# Further, you can replace classes in the tree with subclasses to add customization,
# e.g., converting data-types into more python friendly fromats


@dataclass
class MyImage(v18.Sensor.Camera.Image):
    image_dim: Tuple[int, int] = field(init=False)

    def __post_init__(self):
        self.image_dim = (
            sdf_root.model.link[0].sensor[0].camera.image.height,
            sdf_root.model.link[0].sensor[0].camera.image.width,
        )


v18_string: v18.Sdf = ign.sdformat.loads(
    sdf_string, custom_constructor={v18.Sensor.Camera.Image: MyImage}
)

#%%
# and now every camera in the parsed SDF will have a ``image_dim`` property which you can use

camera = v18_string.model.link[0].sensor[0].camera
print(f"The camera resolution is: {camera.image.image_dim}")

#%%
# How do you know which class to overwrite? Scikit-bot's binding layout follows
# the layout of the spec. On the `spec's website <http://sdformat.org/spec>`_
# you can find several tabs, each representing a SDF element. Each tab then
# lists a tree of sub-elements and where they can appear. The data-bindings have
# the same layout, with exception of ``Model``, which is called ``ModelModel``
# and ``State.Model`` which is called ``StateModel``. This is done to avoid a
# name collision in both the bindings and the XSD schemata. Alternatively, you
# can look up each attribute in the binding's `API documentation
# <https://scikit-bot.org/en/latest/_autosummary/skbot.ignition.html#sdformat-xml>`_.
#
# Writing / Serialization
# -----------------------
#
# Of course scikit-bot can also turn SDF object trees back into SDF strings.
# Just like before, scikit-bot converts the tree into a string, which you can
# then write to file, should you wish to do so.

result_string = ign.sdformat.dumps(sdf_root)
print(result_string)

# %%
# Note that the resulting SDF string differs from the original SDF string in two
# ways: (1) default values have been set explicitly, and (2) all unneeded
# white-space is removed. To get a neatly-formatted, human-readable string you
# have to set the ``format=True`` flag.

ign.sdformat.dumps(sdf_root, format=True)

#%%
#
# Building SDF from Scratch
# -------------------------
#
# Finally, you can use explicitly instantiate SDF objects and build your own file.


#%%

# declarative style
# nesting objects inside the constructor
ground_plane = v18.model.Model(
    static=True,
    name="ground_plane",
    link=[
        v18.Link(
            collision=v18.Collision(
                v18.Geometry(plane=v18.Geometry.Plane(normal="1 0 0", size="1.4 6.3"))
            ),
            visual=v18.Visual(
                v18.Geometry(plane=v18.Geometry.Plane(normal="0 1 0", size="2 4"))
            ),
        )
    ],
)

# # procedual style
# box = v18.model.Model()
# box.pose = v18.model.Model.Pose("0 0 2.5 0 0 0", relative_to="ground_plane")
# box.link.append(v18.Link())  # link is a list; a model can have many links
# box.link[0].name = "link"
# # set-up collision
# box.link[0].collision.append(v18.Collision())
# box.link[0].collision[0].name = "collision"
# box.link[0].collision[0].geometry = v18.Geometry.Box("1 2 3")
# box.link[0].collision[0].surface = v18.Collision.Surface()
# box.link[0].collision[0].surface.contact = v18.Collision.Surface.Contact(
#     collide_bitmask=171
# )
# # set-up visual
# box.link[0].visual.append(v18.Visual())
# box.link[0].visual[0].name = "box_vis"
# box.link[0].visual[0].geometry = v18.Geometry.Box("1 2 3")

# root = v18.Sdf(world=[v18.World(name="shapes_world", model=[ground_plane, box])])

# # elements are populated with default values where applicable
# print(f"Gravity set to: {root.world[0].gravity}")
# # Gravity set to: 0 0 -9.8

# # and of course you can serialize to SDF
# sdf_string = ign.sdformat.dumps(root, format=True)

# # and write the string into a file
# Path("my_world.sdf").write_text(sdf_string)

# # or (more old-school) via open(...)
# with open("my_world.sdf", "w") as sdf_file:
#     print(sdf_string, file=sdf_file)


# # loading is similary straight forward
# sdf_string = Path("my_world.sdf").read_text()
# root = ign.sdformat.loads(sdf_string)

# # or again via open(...)
# with open("my_world.sdf", "r") as sdf_file:
#     sdf_string = sdf_file.read()
# root = ign.sdformat.loads(sdf_string)

# # Note that scikit-bot will by default auto-detect the SDF version from sdf's version
# # attribute (all versions are supported). Alternatively, you can manually
# # overwrite the auto-detect with a specific version.
# sdf_reloaded = ign.sdformat.reads(sdf_string, version="1.6")

# # you can assign the same object in multiple places to link the properties
# box_geometry = v18.Geometry()
# box_geometry.box = v18.Geometry.Box("1 2 3")
# box.link[0].collision[0].geometry = box_geometry
# box.link[0].visual[0].geometry = box_geometry

# # and change both properties at the same time
# box_geometry.box.size = "2 5 2"
# print(ign.sdformat.dumps(root, format=True))

# # however this linking will (of course) not survive serialization.
