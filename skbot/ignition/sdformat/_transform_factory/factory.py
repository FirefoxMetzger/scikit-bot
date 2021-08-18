from skbot.ignition.messages import Model
from typing import Callable, Dict, Union, List, Any
import importlib
from urllib.parse import urlparse
from requests.exceptions import RequestException

from .. import sdformat
from .scopes import LightScope, ModelScope, Scope, WorldScope
from ...fuel import get_fuel_model
from .... import transform as tf
from .generic import GenericInclude, GenericJoint, GenericLight, GenericLink, GenericModel, GenericSensor, GenericWorld
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
            root_uri = self.root_uri
            rel_path = uri
        else:
            raise sdformat.ParseError(f"Unknown URI: {uri}")

        try:
            sdf = get_fuel_model(root_uri, file_path=rel_path)
        except RequestException:
            raise sdformat.ParseError(f"Unable to read '{str(rel_path)}' from '{str(root_uri)}'")
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
            frame = tf.Frame(3, name=collision.name)
            scaffold_frame = tf.Frame(3, name=collision.name)
            scope.add_scaffold(
                scaffold_frame, collision.pose.value, collision.pose.relative_to
            )
            scope.declare_link(DynamicPose(link.name, frame, scaffold_child=scaffold_frame))

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

        if model.canonical_link is None:
            raise sdformat.ParseError(f"Unable to determine canonical link for model '{model.name}'")

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

        # TODO: actor
        # TODO: road
        # TODO: spherical coords
        # TODO: state
        # TODO: population

        # # convert population
        # for population in world.population:
        #     tf_frame = tf.Frame(3, name=population.name)
        #     offset = _pose_to_numpy(population.pose.value)
        #     tf_link = tf.Translation(offset)

        #     if population.pose.relative_to is not None:
        #         parent = population.pose.relative_to
        #         unresolved_poses.append((parent, tf_frame, tf_link))
        #     else:
        #         tf_link(tf_frame, world_frame)

        #     num_defined = 0
        #     if population.box is not None:
        #         num_defined += 1
        #     if population.cylinder is not None:
        #         num_defined += 1
        #     num_defined += len(population.model)

        #     if len(population.model) > 1:
        #         raise NotImplementedError("Multiple models defined for population..")
        #     elif num_defined == 0:
        #         raise sdformat.ParseError("No models defined for population.")

        #     if population.box:
        #         model_gen = lambda: tf.Frame(3)
        #     elif population.cylinder:
        #         model_gen = lambda: tf.Frame(3)
        #     else:
        #         model_gen = lambda: _convert_model(population.model[0])

        #     step = np.array(population.distribution.step.split(" "), dtype=float)
        #     rows = np.arange(population.distribution.rows)[:, -1, -1]
        #     cols = np.array(population.distribution.cols)[-1, :, -1]

        #     dist_kind = population.distribution.type
        #     if dist_kind == "random":
        #         for _ in range(population.model_count):
        #             tf_frame = model_gen()
        #             # TODO: randomize me
        #             tf_link = tf.Translation((0, 0, 0))
        #             tf_link(tf_frame, world_frame)
        #     elif dist_kind == "uniform":
        #         pass
        #     elif dist_kind == "grid":
        #         row_step, col_step, _ = [
        #             float(x) for x in population.distribution.step.split(" ")
        #         ]
        #         for row in range(population.distribution.rows):
        #             row_pos = row_step * row
        #             for col in range(population.distribution.cols):
        #                 col_pos = col_step * col
        #                 tf_frame = model_gen()
        #                 tf_frame.name = tf_frame.name + f"_clone_{col*population.distribution.rows + row}"
        #                 tf_link = tf.Translation((row_pos, col_pos, 0))
        #     elif dist_kind == "linear-x":
        #         raise NotImplementedError("Linear placement not implemented yet.")
        #     elif dist_kind == "linear-y":
        #         raise NotImplementedError("Linear placement not implemented yet.")
        #     elif dist_kind == "linear-z":
        #         raise NotImplementedError("Linear placement not implemented yet.")

        #     for model_idx in range(population.model_count):
        #         pass

        return world_scope
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
