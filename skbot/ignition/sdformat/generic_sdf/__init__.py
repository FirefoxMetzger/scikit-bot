""" Version-Agnostic SDF Bindings

.. currentmodule:: skbot.ignition.sdformat.generic_sdf

.. warning::
    This module is experimental and not all SDFormat elements are currently
    supported. If an element is not supported, it will raise a warning. To
    suppress this warning use::

        skbot.ignition.sdformat.generic_sdf.base.WARN_UNSUPPORTED = False
    

This module contains version-agnostic bindings for `SDFormat
<http://sdformat.org/spec>`_. The idea of these bindings is that they can parse
SDF in any one version, and allow you to consume the SDF as if it were any other
SDF version. 

This, of course, comes with the limitation of compatibility between versions.
For example, you can load a SDF v1.6 file and access elements introduced in SDF
v1.8 if they have a default value or can be computed from the values available.
However, if an element is now required in SDF v1.8 but wasn't available in SDF
v1.6 then it will not be set. Further, if an element is no longer available in
the most recent SDF version, it will raise a depreciation warning. Such cases
will be documented as such.

In addition to unavoidable version incompatibilities listed above, the bindings
make the following oppinionated decisions:

    - Some variable names differ from SDFormat

        - If an element may have multiple children of the same kind, they
          corresponding attribute uses plural instead of singular, e.g.
          ``models`` instead of ``model``.
        - If different SDF versions use different names for the same variable,
          they are converted into the name used in the most recent SDFormat
          version. Old names are still available via a @property and will raise
          a depreciation warning.

    - vectors are converted to numpy arrays
    - includes are resolved, removes, and the included element is inserted
      instead
    - __model__ is appended to frame references where necessary, e.g., a
      reference of the form ``model_A::model_B`` will become 
      ``model_A::model_b:__model__``.

Supported Elements
------------------

.. autosummary::
    :toctree: generic_sdf

    sdf.Sdf
    camera.Camera
    frame.Frame
    joint.Joint
    link.Link
    model.Model
    sensor.Sensor
    world.World
    include.Include
    origin.Origin


Unsupported Elements
--------------------

The following elements are currently recognized, but not implemented. When encountered,
they will raise a warning.

.. autosummary::
    :toctree: generic_sdf

    state.State
    light_state.Light
    link_state.Link
    model_state.Model
    collision.Collision
    inertial.Inertial
    material.Material
    geometry.Geometry
    visual.Visual
    actor.Actor
    audio_sink.AudioSink
    audio_source.AudioSource
    collision_engine.CollisionEngine
    gripper.Gripper
    particle_emitter.ParticleEmitter
    physics.Physics
    scene.Scene
    surface.Surface
    urdf.URDF


.. rubric:: Sensors

.. autosummary::
    :toctree: generic_sdf

    sensors.Lidar
    sensors.Ray
    sensors.AirPressure
    sensors.Altimeter
    sensors.Contact
    sensors.ForceTorque
    sensors.Gps
    sensors.Imu
    sensors.LogicalCamera
    sensors.Magnetometer
    sensors.Navsat
    sensors.RfidTag
    sensors.Rfid
    sensors.Sonar
    sensors.Transceiver
    light.Light

.. rubric:: Shapes

.. autosummary::
    :toctree: generic_sdf

    shapes.Box
    shapes.Capsule
    shapes.Cylinder
    shapes.Ellipsoid
    shapes.Heightmap
    shapes.Image
    shapes.Mesh
    shapes.Plane

.. rubric:: Misc

.. autosummary::
    :toctree: generic_sdf

    gui.Gui
    atmosphere.Atmosphere
    battery.Battery
    noise.Noise
    population.Population
    projector.Projector


"""

# currently imported for coverage x)
from . import base, sensors, shapes

# import top-level elements as mentioned in the
# SDFormat spec.
from .actor import Actor
from .collision import Collision
from .geometry import Geometry
from .joint import Joint
from .light import Light
from .link import Link
from .material import Material
from .model import Model
from .physics import Physics
from .scene import Scene
from .sensor import Sensor
from .state import State
from .visual import Visual
from .world import World

__all__ = [
    "World",
    "Scene",
    "State",
    "Physics",
    "Light",
    "Actor",
    "Model",
    "Link",
    "Sensor",
    "Joint",
    "Collision",
    "Visual",
    "Material",
    "Geometry",
]
