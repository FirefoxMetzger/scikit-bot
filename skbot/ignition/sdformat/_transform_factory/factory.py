from skbot.transform import joints
from typing import Callable, Dict, Union, List, Any
import importlib
from urllib.parse import urlparse
from requests.exceptions import RequestException

from .. import sdformat
from .scopes import LightScope, ModelScope, Scope, WorldScope
from ...fuel import get_fuel_model
from .... import transform as tf
from .generic import (
    GenericFrame,
    GenericInclude,
    GenericJoint,
    GenericLight,
    GenericLink,
    GenericModel,
    GenericSensor,
    GenericWorld,
    NamedPoseBearing,
)
from .links import DynamicPose, CustomLink, RotationJoint, PrismaticJoint, SimplePose
from ...transformations import FrustumProjection


# available SDF elements by version
_converter_roots = {
    "1.0": None,
    "1.2": None,
    "1.3": None,
    "1.4": None,
    "1.5": "..v15",
    "1.6": None,
    "1.7": "..v17",
    "1.8": "..v18",
}


class FactoryBase:
    """Frame Graph Factory

    This class constructs a frame graph from a tree of generic SDF objects (see generic.py). It
    is subclassed by the version-specific factories (vXX.py) which implement conversion from
    version-specific SDF objects to generic objects.

    """

    def __init__(self, *, root_uri: str = None):
        self.root_uri: str = root_uri

    def __call__(self, sdf: str) -> Union[Scope, List[Scope]]:
        raise NotImplementedError()

    def _resolve_include(self, uri: str) -> ModelScope:
        # there is only one fuel server
        fuel_server = "fuel.ignitionrobotics.org"
        uri_parts = urlparse(uri)

        if uri_parts.scheme == "https" and uri_parts.netloc == fuel_server:
            root_uri = uri
            rel_path = "model.sdf"
        elif uri_parts.scheme == "model":
            raise NotImplementedError("Unsure how to resolve model://.")
        elif uri_parts.scheme == "":
            root_uri = self.root_uri
            rel_path = uri
        else:
            raise sdformat.ParseError(f"Unknown URI: {uri}")

        try:
            sdf = get_fuel_model(root_uri, file_path=rel_path)
        except RequestException:
            raise sdformat.ParseError(
                f"Unable to read '{str(rel_path)}' from '{str(root_uri)}'"
            )
        return transform_factory(sdf, root_uri=root_uri)[0]

    def _convert_frame(self, scope: "Scope", frame: GenericFrame):
        scope.declare_frame(frame.name)
        scope.add_scaffold(frame.name, frame.pose.value, frame.pose.relative_to)

        if frame.attached_to is None:
            scope.declare_link(DynamicPose(scope.default_frame, frame.name))
        else:
            scope.declare_link(DynamicPose(frame.attached_to, frame.name))

    def convert_sensor(
        self, sensor: GenericSensor, scope: Scope, attached_to: NamedPoseBearing
    ) -> tf.Frame:
        sensor_frame = tf.Frame(3, name=sensor.name)
        sensor_scaffold = tf.Frame(3, name=sensor.name)
        scope.add_scaffold(sensor_scaffold, sensor.pose.value, sensor.pose.relative_to)
        scope.declare_link(
            DynamicPose(attached_to.name, sensor_frame, scaffold_child=sensor_scaffold)
        )

        if sensor.type == "air_pressure":
            raise NotImplementedError()
        elif sensor.type == "altimeter":
            raise NotImplementedError()
        elif sensor.type == "camera":
            pose = sensor.camera.pose
            camera_frame = tf.Frame(3, name="camera-space")
            camera_scaffold = tf.Frame(3, name="camera-space")
            scope.add_scaffold(camera_scaffold, pose.value, pose.relative_to)
            scope.declare_link(
                DynamicPose(
                    sensor_frame,
                    camera_frame,
                    scaffold_parent=sensor_scaffold,
                    scaffold_child=camera_scaffold,
                )
            )
            scope.declare_link(
                CustomLink(
                    camera_frame,
                    tf.Frame(2, name="pixel-space"),
                    FrustumProjection(
                        sensor.camera.horizontal_fov,
                        (sensor.camera.image.height, sensor.camera.image.width),
                    ),
                )
            )

            for frame in sensor.camera.frames:
                self._convert_frame(scope, frame)

        elif sensor.type == "contact":
            raise NotImplementedError()
        elif sensor.type == "depth_camera":
            raise NotImplementedError()
        elif sensor.type == "force_torque":
            raise NotImplementedError()
        elif sensor.type == "gps":
            raise NotImplementedError()
        elif sensor.type == "gpu_lidar":
            raise NotImplementedError()
        elif sensor.type == "gpu_ray":
            raise NotImplementedError()
        elif sensor.type == "imu":
            raise NotImplementedError()
        elif sensor.type == "lidar":
            raise NotImplementedError()
        elif sensor.type == "logica_camera":
            raise NotImplementedError()
        elif sensor.type == "magnetometer":
            raise NotImplementedError()
        elif sensor.type == "multicamera":
            raise NotImplementedError()
        elif sensor.type == "rfid":
            raise NotImplementedError()
        elif sensor.type == "rfidtag":
            raise NotImplementedError()
        elif sensor.type == "rgbd_camera":
            raise NotImplementedError()
        elif sensor.type == "sonar":
            raise NotImplementedError()
        elif sensor.type == "thermal_camera":
            raise NotImplementedError()
        elif sensor.type == "wireless_receiver":
            raise NotImplementedError()
        elif sensor.type == "wireless_transmitter":
            raise NotImplementedError()
        else:
            raise sdformat.ParseError(f"Unkown sensor type: {sensor.type}")

        for frame in sensor.frames:
            self._convert_frame(scope, frame)

        return sensor_scaffold

    def convert_joint(self, joint: GenericJoint, scope: ModelScope):
        scope.declare_frame(joint.name)
        scope.add_scaffold(joint.name, joint.pose.value, joint.pose.relative_to)
        scope.declare_link(DynamicPose(joint.child, joint.name))

        joint_parent = tf.Frame(3, name=joint.name + "_parent")
        scope.declare_link(
            DynamicPose(joint_parent, joint.parent, scaffold_parent=joint.name)
        )

        if joint.type == "revolute":
            scope.declare_link(
                RotationJoint(
                    joint.name,
                    joint_parent,
                    joint.axis.xyz.value,
                    joint.axis.xyz.expressed_in,
                    joint.axis.limit.lower,
                    joint.axis.limit.upper,
                )
            )
        elif joint.type == "hinge":
            raise NotImplementedError("Hinge joints have not been added yet.")
        elif joint.type == "gearbox":
            raise NotImplementedError("Gearbox joints have not been added yet.")
        elif joint.type == "revolute2":
            raise NotImplementedError("Revolute2 type joint is not added yet.")
        elif joint.type == "prismatic":
            scope.declare_link(
                PrismaticJoint(
                    joint.name,
                    joint_parent,
                    joint.axis.xyz.value,
                    joint.axis.xyz.expressed_in,
                    joint.axis.limit.lower,
                    joint.axis.limit.upper,
                )
            )
        elif joint.type == "ball":
            raise NotImplementedError("Ball joints have not been added yet.")
        elif joint.type == "screw":
            raise NotImplementedError("Screw joints have not been added yet.")
        elif joint.type == "universal":
            raise NotImplementedError("Universal joints have not been added yet.")
        elif joint.type == "fixed":
            scope.declare_link(
                DynamicPose(joint.name, joint_parent, scaffold_child=joint.name)
            )
        else:
            raise sdformat.ParseError(f"Unknown Joint type: {joint.type}")

        for sensor in joint.sensor:
            self.convert_sensor(sensor, scope, attached_to=joint)

        for frame in joint.frames:
            self._convert_frame(scope, frame)

        return scope

    def convert_light(self, light: GenericLight, *, scope: Scope = None) -> Scope:
        if scope is None:
            scope = LightScope(light.name)

        for frame in light.frames:
            self._convert_frame(scope, frame)

        scope.declare_frame(light.name)
        scope.add_scaffold(light.name, light.pose.value, light.pose.relative_to)

        return scope

    def convert_link(self, link: GenericLink, scope: Scope) -> Scope:
        if link.must_be_base_link:
            link.pose.relative_to = "world"
            scope.declare_link(DynamicPose("world", link.name))

        scope.declare_frame(link.name)
        scope.add_scaffold(link.name, link.pose.value, link.pose.relative_to)

        if link.inertial:
            scope.declare_link(
                SimplePose(
                    link.name, tf.Frame(3, name="inertial"), link.inertial.pose.value
                )
            )

        for collision in link.collision:
            frame = tf.Frame(3, name=collision.name)
            scaffold_frame = tf.Frame(3, name=collision.name)
            scope.add_scaffold(
                scaffold_frame, collision.pose.value, collision.pose.relative_to
            )
            scope.declare_link(
                DynamicPose(link.name, frame, scaffold_child=scaffold_frame)
            )

        for visual in link.visual:
            frame = tf.Frame(3, name=visual.name)
            scaffold_frame = tf.Frame(3, name=visual.name)
            scope.add_scaffold(
                scaffold_frame, visual.pose.value, visual.pose.relative_to
            )
            scope.declare_link(
                DynamicPose(link.name, frame, scaffold_child=scaffold_frame)
            )

        for sensor in link.sensors:
            self.convert_sensor(sensor, scope, attached_to=link)

        if link.projector:
            frame = tf.Frame(3, name=link.projector.name)
            scaffold_frame = tf.Frame(3, name=link.projector.name)
            scope.add_scaffold(
                scaffold_frame,
                link.projector.pose.value,
                link.projector.pose.relative_to,
            )
            scope.declare_link(
                DynamicPose(link.name, frame, scaffold_child=scaffold_frame)
            )
            # TODO: there might be a link into the projected frame missing
            # here I don't exactly know how projector works and didn't find
            # docs

        for idx, source in enumerate(link.audio_sources):
            name = link.name + f"-audio-source-{idx}"
            scope.declare_frame(name)
            scope.add_scaffold(name, source.pose.value, source.pose.relative_to)
            scope.declare_link(DynamicPose(link.name, name))

        for light in link.lights:
            self.convert_light(light, scope=scope)
            scope.declare_link(DynamicPose(link.name, light.name))

        for frame in link.frames:
            self._convert_frame(scope, frame)

        return scope

    def convert_model(
        self, model: GenericModel, *, parent_scope: Scope = None
    ) -> Scope:
        scope = ModelScope(
            model.name,
            placement_frame=model.placement_frame,
            canonical_link=model.canonical_link,
        )

        scope.pose = model.pose

        for link in model.links:
            self.convert_link(link, scope)

        for include in model.include:
            self.resolve_include(include, scope)

            # double-check if this is correct
            scope.add_scaffold(include.name, "0 0 0 0 0 0")
            scope.declare_link(
                SimplePose(scope.default_frame, include.name, "0 0 0 0 0 0")
            )

        for nested_model in model.models:
            self.convert_model(nested_model, parent_scope=scope)

            # double-check if this is correct
            scope.add_scaffold(nested_model.name, "0 0 0 0 0 0")
            scope.declare_link(
                SimplePose(scope.default_frame, nested_model.name, "0 0 0 0 0 0")
            )

        for frame in model.frames:
            scope.declare_frame(frame.name)
            scope.add_scaffold(frame.name, frame.pose.value, frame.pose.relative_to)
            if frame.attached_to == "__model__":
                scope.declare_link(DynamicPose(scope.canonical_link, frame.name))
            else:
                scope.declare_link(DynamicPose(frame.attached_to, frame.name))

        for joint in model.joints:
            self.convert_joint(joint, scope)

        if parent_scope is not None:
            parent_scope.add_subscope(scope)
            parent_scope.declare_frame(model.name)
            child = scope.name + "::" + scope.placement_frame

            if model.pose.relative_to is None:
                model.pose.relative_to = model.name

            parent_scope.add_scaffold(child, model.pose.value, model.pose.relative_to)

        if scope.canonical_link is None:
            raise sdformat.ParseError(
                f"Unable to determine canonical link for model '{model.name}'"
            )

        return scope

    def resolve_include(self, include: GenericInclude, scope: Scope) -> None:
        subscope = self._resolve_include(include.uri)

        if include.name is None:
            include.name = subscope.name

        name = include.name
        subscope.name = include.name
        scope.add_subscope(subscope)
        scope.declare_frame(name)

        if isinstance(scope, ModelScope):
            if scope.canonical_link is None:
                scope.canonical_link = name

        if include.placement_frame is not None:
            placement_frame = include.placement_frame
        else:
            placement_frame = subscope.placement_frame
            # TODO: deal with absend //include/pose
            # not quite sure how yet.

        if include.pose is None:
            include.pose = subscope.pose

        if include.pose.relative_to is None:
            include.pose.relative_to = name

        placement_frame = subscope.name + "::" + placement_frame

        scope.add_scaffold(
            placement_frame, include.pose.value, include.pose.relative_to
        )

        child = subscope.name + "::" + subscope.canonical_link
        scope.declare_link(DynamicPose(name, child))

    def convert_world(self, world: GenericWorld) -> Scope:
        world_scope = WorldScope(world.name)
        for include in world.includes:
            self.resolve_include(include, world_scope)

            # double-check if this is correct
            world_scope.add_scaffold(include.name, "0 0 0 0 0 0")
            world_scope.declare_link(SimplePose("world", include.name, "0 0 0 0 0 0"))

        # TODO: GUI
        # TODO: scene

        for light in world.lights:
            self.convert_light(light, scope=world_scope)

            # not sure if this is valid
            world_scope.declare_link(DynamicPose("world", light.name))

        for frame in world.frames:
            world_scope.declare_frame(frame.name)
            world_scope.add_scaffold(
                frame.name, frame.pose.value, frame.pose.relative_to
            )

            if frame.attached_to is None:
                frame.attached_to = "world"
            elif frame.attached_to == "":
                frame.attached_to = "world"

            world_scope.declare_link(DynamicPose(frame.attached_to, frame.name))

        for model in world.models:
            self.convert_model(model, parent_scope=world_scope)

            # double-check if this is correct
            world_scope.add_scaffold(model.name, "0 0 0 0 0 0")
            world_scope.declare_link(SimplePose("world", model.name, "0 0 0 0 0 0"))

            link_name = model.name + "::" + model.canonical_link
            world_scope.declare_link(DynamicPose(model.name, link_name))

        # TODO: actor
        # TODO: road
        # TODO: spherical coords
        # TODO: state
        # TODO: population

        return world_scope


class TransformFactory:
    """A factory that turns SDF of different versions into generic graphs
    that can then be assembled into transform graphs"""

    converters: Dict[str, Callable[[Any], Union[Scope, List[Scope]]]] = dict()

    def __call__(self, sdf: str, *, root_uri: str = None) -> Scope:
        version = sdformat.get_version(sdf)
        if version not in self.converters.keys():
            # lazy loading of SDF bindings
            converter_module = _converter_roots[version]
            if converter_module is None:
                raise NotImplementedError(f"SDFormat v{version} is not supported yet.")
            mod = importlib.import_module(converter_module, __name__)
            self.converters[version] = mod.Converter

        return self.converters[version](root_uri=root_uri)(sdf)


# a singleton
transform_factory = TransformFactory()
