import skbot.ignition as ign
from skbot.ignition.sdformat.bindings import v18
from pathlib import Path

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
