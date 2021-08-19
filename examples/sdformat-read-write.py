""" 

Reading and Writing SDFormat XML
================================

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

Importing the Bindings
----------------------
"""
#%%

import skbot.ignition as ign
from skbot.ignition.sdformat.bindings import v18
from pathlib import Path

#%%
# The SDFormat bindings are part of scikit-bot's :mod:`ignition
# module<skbot.ignition>`. The ignition module has additional dependencies, and
# - as such - you will have to install these as well. instructions on how to do
# this can be found in the :mod:`module's documentation`.
# 
# Another thing to note is that the SDFormat bindings are not imported together
# with the ignition module. This is a conscious choice, as the bindings for each
# versions are quite large. To keep import times low, the version-specific
# bindings are lazy-loaded whenever scikit-bot needs them or when you import
# them explicitly::
#
#     from skbot.ignition.sdformat.bindings import vXX
#
# where ``vXX``` is the version you wish to use. In this example we use ``v18``.
#
# Reading / Loading
# -----------------
#
# .. note::
#     You don't have to explicitly import bindings to load SDF. The required
#     version will be lazy-loaded for you.
#
# Scikit-bot reads SDFormat from strings containing valid XML. While we might support directly reading from file
# in the future, pythons built-in ability to read files and manage the filesystem are very extensive and there
# is little you can't accomplish in one or two lines. YOu can find examples of this below.
#
# Let's start with a small SDF string.
#%%

sdf_string = (
    """
    """
)


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

# procedual style
box = v18.model.Model()
box.pose = v18.model.Model.Pose("0 0 2.5 0 0 0", relative_to="ground_plane")
box.link.append(v18.Link())  # link is a list; a model can have many links
box.link[0].name = "link"
# set-up collision
box.link[0].collision.append(v18.Collision())
box.link[0].collision[0].name = "collision"
box.link[0].collision[0].geometry = v18.Geometry.Box("1 2 3")
box.link[0].collision[0].surface = v18.Collision.Surface()
box.link[0].collision[0].surface.contact = v18.Collision.Surface.Contact(
    collide_bitmask=171
)
# set-up visual
box.link[0].visual.append(v18.Visual())
box.link[0].visual[0].name = "box_vis"
box.link[0].visual[0].geometry = v18.Geometry.Box("1 2 3")

root = v18.Sdf(world=[v18.World(name="shapes_world", model=[ground_plane, box])])

# elements are populated with default values where applicable
print(f"Gravity set to: {root.world[0].gravity}")
# Gravity set to: 0 0 -9.8

# and of course you can serialize to SDF
sdf_string = ign.sdformat.dumps(root, format=True)

# and write the string into a file
Path("my_world.sdf").write_text(sdf_string)

# or (more old-school) via open(...)
with open("my_world.sdf", "w") as sdf_file:
    print(sdf_string, file=sdf_file)


# loading is similary straight forward
sdf_string = Path("my_world.sdf").read_text()
root = ign.sdformat.loads(sdf_string)

# or again via open(...)
with open("my_world.sdf", "r") as sdf_file:
    sdf_string = sdf_file.read()
root = ign.sdformat.loads(sdf_string)

# Note that scikit-bot will by default auto-detect the SDF version from sdf's version
# attribute (all versions are supported). Alternatively, you can manually
# overwrite the auto-detect with a specific version.
sdf_reloaded = ign.sdformat.reads(sdf_string, version="1.6")

# you can assign the same object in multiple places to link the properties
box_geometry = v18.Geometry()
box_geometry.box = v18.Geometry.Box("1 2 3")
box.link[0].collision[0].geometry = box_geometry
box.link[0].visual[0].geometry = box_geometry

# and change both properties at the same time
box_geometry.box.size = "2 5 2"
print(ign.sdformat.dumps(root, format=True))

# however this linking will (of course) not survive serialization.
