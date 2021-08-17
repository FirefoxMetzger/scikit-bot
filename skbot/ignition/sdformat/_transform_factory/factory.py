from typing import Callable, Dict, Union, List, Any
import importlib
from urllib.parse import urlparse

from .. import sdformat
from .scopes import LightScope, ModelScope, Scope
from ...fuel import get_fuel_model
from .... import transform as tf
from .generic import GenericJoint, GenericLight, GenericLink, GenericSensor
from .links import DynamicPose, CustomLink, RotationJoint, PrismaticJoint, SimplePose


# available SDF elements by version
_converter_roots = {
    "1.0": None,
    "1.2": None,
    "1.3": None,
    "1.4": None,
    "1.5": None,
    "1.6": None,
    "1.7": "..v17",
    "1.8": "..v18",
}


class FactoryBase:
    def __init__(self, *, unwrap=True, root_uri: str = None):
        self.root_uri: str = root_uri
        self.unwrap: bool = unwrap

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
            rel_path = uri
        else:
            raise sdformat.ParseError(f"Unknown URI: {uri}")

        sdf = get_fuel_model(root_uri, file_path=rel_path)
        return transform_factory(sdf, root_uri=root_uri)

    def convert_sensor(self, sensor: GenericSensor, scope: Scope) -> Scope:
        scope.declare_frame(sensor.name)
        scope.add_scaffold(sensor.name, sensor.pose.value, sensor.pose.relative_to)

        if sensor.type == "air_pressure":
            raise NotImplementedError()
        elif sensor.type == "alimeter":
            raise NotImplementedError()
        elif sensor.type == "camera":
            if sensor.camera.noise is not None:
                raise NotImplementedError()
            if sensor.camera.distortion is not None:
                raise NotImplementedError()
            if sensor.camera.lens is not None:
                raise NotImplementedError()

            name = sensor.name + "-camera-space"
            pose = sensor.camera.pose
            scope.declare_frame(name)
            scope.add_scaffold(name, pose.value, pose.relative_to)
            scope.declare_link(DynamicPose(sensor.name, name))

            scope.declare_link(
                CustomLink(
                    sensor.name,
                    tf.Frame(2, name="pixel-space"),
                    tf.FrustumProjection(
                        sensor.camera.horizontal_fov,
                        (sensor.camera.image.height, sensor.camera.image.width),
                    ),
                )
            )
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

        return scope

    def convert_joint(self, joint: GenericJoint, scope: Scope) -> Scope:
        scope.declare_frame(joint.name)
        scope.add_scaffold(joint.name, joint.pose.value, joint.pose.relative_to)
        scope.declare_link(DynamicPose(joint.child, joint.name))

        if joint.type == "revolute":
            scope.declare_link(
                RotationJoint(
                    joint.name,
                    joint.parent,
                    joint.axis.xyz.value,
                    joint.axis.xyz.expressed_in,
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
                    joint.parent,
                    joint.axis.xyz.value,
                    joint.axis.xyz.expressed_in,
                )
            )
        elif joint.type == "ball":
            raise NotImplementedError("Ball joints have not been added yet.")
        elif joint.type == "screw":
            raise NotImplementedError("Screw joints have not been added yet.")
        elif joint.type == "universal":
            raise NotImplementedError("Universal joints have not been added yet.")
        elif joint.type == "fixed":
            scope.declare_link(DynamicPose(joint.name, joint.parent))

        for sensor in joint.sensor:
            self.convert_sensor(sensor, scope)
            scope.declare_link(DynamicPose(joint.name, sensor.name))

        return scope

    def convert_light(self, light: GenericLight, *, scope: Scope = None) -> Scope:
        if scope is None:
            scope = LightScope(light.name)

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
            scope.declare_frame(collision.name)
            scope.add_scaffold(
                collision.name, collision.pose.value, collision.pose.relative_to
            )
            scope.declare_link(DynamicPose(link.name, collision.name))

        for visual in link.visual:
            scope.declare_frame(visual.name)
            scope.add_scaffold(visual.name, visual.pose.value, visual.pose.relative_to)
            scope.declare_link(DynamicPose(link.name, visual.name))

        for sensor in link.sensors:
            self.convert_sensor(sensor, scope)
            scope.declare_link(DynamicPose(link.name, sensor.name))

        if link.projector:
            scope.declare_frame(link.projector.name)
            scope.add_scaffold(
                link.projector.name,
                link.projector.pose.value,
                link.projector.pose.relative_to,
            )
            scope.declare_link(DynamicPose(link.name, link.projector.name))
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

        return scope


class TransformFactory:
    """A factory that turns SDF of different versions into generic graphs
    that can then be assembled into transform graphs"""

    converters: Dict[str, Callable[[Any], Union[Scope, List[Scope]]]] = dict()

    def __call__(self, sdf: str, *, unwrap=True, root_uri: str = None) -> Scope:
        version = sdformat.get_version(sdf)
        if version not in self.converters.keys():
            # lazy loading of SDF bindings
            converter_module = _converter_roots[version]
            if converter_module is None:
                raise NotImplementedError(f"SDFormat v{version} is not supported yet.")
            mod = importlib.import_module(converter_module, __name__)
            self.converters[version] = mod.Converter

        return self.converters[version](root_uri=root_uri, unwrap=unwrap)(sdf)


# a singleton
transform_factory = TransformFactory()
