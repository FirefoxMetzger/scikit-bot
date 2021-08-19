""" 

Reading and Writing SDFormat XML
================================

.. currentmodule:: skbot.ignition

"""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# create the thumbnail image for this example
header = mpimg.imread("sdformat-read-write-thumb.png")
fig, ax = plt.subplots(figsize=(3, 3), dpi=80)
ax.imshow(header)
ax.axis('off')
fig.show()

# %%
#Scikit-bot comes with bindings and schemata to read and write SDFormat. SDFormat
#(Simulation Description Format) is a - pretty extensive - XML format that is
#primarily intended to describe simulation worlds and robots. It was originially
#developed for the `Gazebo simulator <http://gazebosim.org/>`_ (now superseeded by
#`Ignition Gazebo <https://ignitionrobotics.org/home>`_) and is developed by
#Ignition robotics. If you are unfamiliar with SDFormat, take a look at their
#`official website <http://sdformat.org/>`_ and check the specification and
#documentation.
#
#The bindings provided by scikit-bot aim to help you write and modify SDFormat
#files, and to allow python code to consume SDF files in a natural manner.
#Examples for the former are (a) validation and verification of existing SDF, or
#(b) procedual generation of SDF files for simulation. An example for the latter
#is scikit-bot itself, which can build a frame graph from SDF, which - among
#other things - gives you easy access to things like forward kinematics.
#
#.. note::
#    While this example is primarily concerned with reading/writing SDF in
#    python, it is worthwhile to point out that scikit-bot ships with XSD1.1
#    bindings for SDFormat. You can find them in your module folder or `here on
#    GitHub
#    <https://github.com/FirefoxMetzger/scikit-bot/tree/main/skbot/ignition/sdformat/schema>`_.
#
#
# Importing the Bindings
# ----------------------
#

from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple

import skbot.ignition as ign
from skbot.ignition.sdformat.bindings import v18

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
            <camera name="awesome_camera">
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

img_dims = (
    sdf_root.model.link[0].sensor[0].camera.image.height,
    sdf_root.model.link[0].sensor[0].camera.image.width,
)
print(f"The camera resolution is: {img_dims}")

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
print(f"Forced version loading: {type(v17_string)}")
print(f"Default version loading: {type(sdf_root)}")

#%%
# As you can see, the object tree was built out of objects from the v1.7 bindings;
# which were imported on-demand.
#
# Sometimes, you may wish to check the version of a SDF string programatically
# without loading any bindings. In such cases you can use the function below. It
# will be faster for large SDF compared to fully parsing it, since it doesn't
# parse the entire string; only until the opening <sdf> element.

ver = ign.sdformat.get_version(sdf_string)

#%%
# Further, you can replace classes in the tree with subclasses to add customization,
# e.g., converting data-types into more python friendly fromats


@dataclass
class MyImage(v18.Sensor.Camera.Image):
    im_shape: Tuple[int, int] = field(init=False)

    def __post_init__(self):
        self.im_shape = (
            sdf_root.model.link[0].sensor[0].camera.image.height,
            sdf_root.model.link[0].sensor[0].camera.image.width,
        )


v18_string: v18.Sdf = ign.sdformat.loads(
    sdf_string, custom_constructor={v18.Sensor.Camera.Image: MyImage}
)

im_shape = v18_string.model.link[0].sensor[0].camera.image.im_shape
print(f"The camera resolution is: {im_shape}")

#%%
# **How do you know which class to overwrite?** Scikit-bot's binding layout follows
# the layout of the spec. On the `spec's website <http://sdformat.org/spec>`_
# you can find several tabs, each representing a SDF element. Each tab then
# lists a tree of sub-elements and where they can appear. The data-bindings have
# the same layout, with exception of ``Model``, which is called ``ModelModel``
# and ``State.Model`` which is called ``StateModel``. This is done to avoid a
# name collision in both the bindings and the XSD schemata. Alternatively, you
# can look up each element in the binding's `API documentation
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

serialized_sdf = ign.sdformat.dumps(sdf_root, format=True)
print(serialized_sdf)

# %%
# Fuel Support
# ------------
#
# One of the more advanced - but very awesome - features of SDF is that you can
# include models from other sources; in particular the `fuel server
# <https://app.ignitionrobotics.org/fuel>`_. This allows you to compose a
# simulation world from several files and re-use them many times.
#
# By default, the parser provided by scikit-bot `does not` auto-include models.
# This is a conscious choice, as we want to remain unoppinionated as to what you
# wish to do with the include tag. You may indeed wish to download the model;
# however, you may alternatively whish to validate a SDF file and need the
# actual include element. Another aspect is that the included model may be
# specified in a different SDFormat version than the one that is currently being
# parsed. Hence, simply copying it into the current object-tree may be a bad
# idea (SDF isn't allways comptible between versions). As such, the bindings
# don't resolve include elements.
#
# That said, you can very easily download and parse nested fuel models using
# scikit-bot::
#
#    sdf_string = """<?xml version="1.0" ?>
#    <sdf version="1.8">
#    <model name="parent_model">
#        <include>
#        <uri>https://fuel.ignitionrobotics.org/1.0/Gambit/models/Pitcher Base</uri>
#        <name>Awesome Pitcher</name>
#        <pose>0 0 0 0 -0 1.5708</pose>
#        </include>
#    </model>
#    </sdf>
#    """
#
#    sdf_root: v18.Sdf = ign.sdformat.loads(sdf_string)
#
#    nested_models = list()
#    for include_el in sdf_root.model.include:
#        nested_sdf = ign.get_fuel_model(include_el.uri)
#        nested_models.append(ign.sdformat.loads(nested_sdf))
#
#    nested_sdf_string = ign.sdformat.dumps(nested_models[0], format=True)
#
#    print(f"The included model:\n{nested_sdf_string}")
#
#
# Building SDF from Scratch
# -------------------------
#
# Finally, we can use the data-bindings explicitly to create an object tree of
# SDF elements that can then be converted into a SDF string.
#
# We can choose a declarative style and nest constructors

ground_plane = v18.model.Model(
    static=True,
    name="ground_plane",
    link=[
        v18.Link(
            name="ground_plane_link",
            collision=v18.Collision(
                geometry=v18.Geometry(
                    plane=v18.Geometry.Plane(normal="1 0 0", size="1.4 6.3")
                )
            ),
            visual=v18.Visual(
                geometry=v18.Geometry(
                    plane=v18.Geometry.Plane(normal="0 1 0", size="2 4")
                )
            ),
        )
    ],
)

# %%
# Or we can use a procedual style that sequentially constructs the objects and
# assigns them.

# create an empty model
box = v18.model.Model()
box.pose = v18.model.Model.Pose("0 0 2.5 0 0 0", relative_to="ground_plane")
box.link.append(v18.Link())  # link is a list; a model can have many links
box.link[0].name = "link"

# set-up collision
box.link[0].collision.append(v18.Collision())
box.link[0].collision[0].name = "collision"
box.link[0].collision[0].geometry = v18.Geometry()
box.link[0].collision[0].geometry.box = v18.Geometry.Box("1 2 3")
box.link[0].collision[0].surface = v18.Collision.Surface()
box.link[0].collision[0].surface.contact = v18.Collision.Surface.Contact(
    collide_bitmask=171
)

# set-up visual
box.link[0].visual.append(v18.Visual())
box.link[0].visual[0].name = "box_vis"
box.link[0].visual[0].geometry = v18.Geometry()
box.link[0].visual[0].geometry.box = v18.Geometry.Box("1 2 3")

# %%
# and once done we can serialize the object tree to string. We can then use
# python to write the resulting string to disk

root = v18.Sdf(
    version="1.8", world=[v18.World(name="shapes_world", model=[ground_plane, box])]
)
sdf_string = ign.sdformat.dumps(root, format=True)
print(sdf_string)

Path("my_world.sdf").write_text(sdf_string)

# or (more old-school) via open(...)
with open("my_world.sdf", "w") as sdf_file:
    print(sdf_string, file=sdf_file)

# %%
# to show the counterpart of the above, this is how you would read SDF from disk

sdf_string = Path("my_world.sdf").read_text()
root = ign.sdformat.loads(sdf_string)

# or again via open(...)
with open("my_world.sdf", "r") as sdf_file:
    sdf_string = sdf_file.read()
root = ign.sdformat.loads(sdf_string)

# %%
# A interesting use-case for manually specifying SDF is that we can let objects
# share child elements and, once we update the properties of the child, they
# will update in all the places where the child is used inside the SDF. Note,
# however, that elements will (of course) not share a child anymore once they
# have been serialized.


box_geometry = v18.Geometry()
box_geometry.box = v18.Geometry.Box("1 2 3")
box.link[0].collision[0].geometry = box_geometry
box.link[0].visual[0].geometry = box_geometry

print(ign.sdformat.dumps(box, format=True))

# %%

box_geometry.box.size = "2 5 2"
print(ign.sdformat.dumps(box, format=True))
