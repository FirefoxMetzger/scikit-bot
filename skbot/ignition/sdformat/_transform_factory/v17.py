from typing import List, Union

from .scopes import Scope, WorldScope, ModelScope
from .links import (
    CustomLink,
    DynamicPose,
    SimplePose,
    RotationJoint,
    PrismaticJoint,
)
from .factory import FactoryBase
from .. import sdformat
from ..bindings import v17
from .... import transform as tf
from .generic import (
    GenericLight,
    GenericPose,
    GenericSensor,
    GenericJoint,
    NamedPoseBearing,
    GenericLink,
    PoseBearing,
)


IncludeElement = Union[v17.ModelModel.Include, v17.World.Include]


class Converter(FactoryBase):
    def __call__(self, sdf: str) -> Union[Scope, List[Scope]]:
        """Convert v1.8 SDF into a Graph

        Parameters
        ----------
        sdf : str
            A string containing v1.8 SDFormat XML.

        Returns
        -------
        graph : _graph.Graph
            A container storing the nodes and edges of the frame graph.

        links : Dict[str, Frames]
            A dict of (named) links in the graph.

        Notes
        -----
        It is necessary to split the parsers, since versions differ so heavily.
        """

        sdf_root: v17.Sdf = sdformat.loads(sdf)
        graph_list: List[Scope] = list()

        for world in sdf_root.world:
            graph = self.convert_world(world)
            graph_list.append(graph)

        for model in sdf_root.model:
            graph = self.convert_model(model)
            graph_list.append(graph)

        for light in sdf_root.light:
            graph = self.convert_light(light)
            graph_list.append(graph)

        if self.unwrap and len(graph_list) == 1:
            return graph_list[0]
        else:
            return graph_list

    def resolve_include(self, include: IncludeElement, scope: Scope) -> None:
        subscope = super()._resolve_include(include.uri)

        if include.name is not None:
            subscope.name = include.name

        name = subscope.name
        scope.add_subscope(subscope)
        scope.declare_frame(name)

        # TODO: deal with absend //include/pose
        # not quite sure how yet.
        if include.pose.relative_to is None:
            include.pose.relative_to = name

        placement_frame = subscope.name + "::" + subscope.placement_frame

        scope.add_scaffold(
            placement_frame, include.pose.value, include.pose.relative_to
        )

        child = subscope.name + "::" + subscope.cannonical_link
        scope.declare_link(DynamicPose(name, child))

    def convert_world(self, world: v17.World) -> Scope:
        world_scope = WorldScope(world.name)
        for include in world.include:
            self.resolve_include(include, world_scope)

        # TODO: GUI
        # TODO: scene

        for light in world.light:
            self.convert_light(light, scope=world_scope)

            # not sure if this is valid
            world_scope.declare_link(DynamicPose("world", light.name))

        for frame in world.frame:
            if frame.pose is None:
                frame.pose = v17.World.Frame.Pose()

            world_scope.declare_frame(frame.name)
            world_scope.add_scaffold(
                frame.name, frame.pose.value, frame.pose.relative_to
            )

            if frame.attached_to is None:
                frame.attached_to = "world"
            elif frame.attached_to == "":
                frame.attached_to = "world"

            world_scope.declare_link(DynamicPose(frame.attached_to, frame.name))

        for model in world.model:
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

    def convert_state(self, state: v17.State) -> Scope:
        raise NotImplementedError()

    def convert_light(self, light: v17.Light, *, scope: Scope = None) -> Scope:
        return super().convert_light(self._to_generic_light(light), scope=scope)

    def convert_actor(self) -> Scope:
        raise NotImplementedError()

    def convert_model(
        self, model: v17.ModelModel, *, parent_scope: Scope = None
    ) -> Scope:
        scope = ModelScope(
            model.name,
            placement_frame=None,
            canonical_link=model.canonical_link,
        )

        if model.pose is None:
            model.pose = v17.ModelModel.Pose()

        scope.pose = model.pose

        for link in model.link:
            if scope.cannonical_link is None:
                scope.cannonical_link = link.name

            self.convert_link(link, scope)

        for include in model.include:
            self.resolve_include(include, scope)

            # double-check if this is correct
            scope.add_scaffold(include.name, "0 0 0 0 0 0")
            scope.declare_link(
                SimplePose(scope.default_frame, include.name, "0 0 0 0 0 0")
            )

        for nested_model in model.model:
            self.convert_model(nested_model, parent_scope=scope)

            # double-check if this is correct
            scope.add_scaffold(nested_model.name, "0 0 0 0 0 0")
            scope.declare_link(
                SimplePose(scope.default_frame, nested_model.name, "0 0 0 0 0 0")
            )

        for frame in model.frame:
            if frame.pose is None:
                frame.pose = v17.ModelModel.Frame.Pose()

            scope.declare_frame(frame.name)
            scope.add_scaffold(frame.name, frame.pose.value, frame.pose.relative_to)

            if frame.attached_to is None:
                frame.attached_to = scope.cannonical_link
            elif frame.attached_to == "":
                frame.attached_to = scope.cannonical_link

            scope.declare_link(DynamicPose(frame.attached_to, frame.name))

        for joint in model.joint:
            self.convert_joint(joint, scope)

        for gripper in model.gripper:
            raise NotImplementedError(
                "Gripper not implemented yet (lacking upstream docs)."
            )

        if parent_scope is not None:
            parent_scope.add_subscope(scope)
            parent_scope.declare_frame(model.name)
            child = scope.name + "::" + scope.placement_frame

            if model.pose.relative_to is None:
                model.pose.relative_to = model.name

            parent_scope.add_scaffold(child, model.pose.value, model.pose.relative_to)

        return scope

    def convert_link(self, link: v17.Link, scope: Scope) -> Scope:
        return super().convert_link(self._to_generic_link(link), scope)

    def convert_sensor(self, sensor: v17.Sensor, scope: Scope) -> Scope:
        generic_sensor = self._to_generic_sensor(sensor)
        return super().convert_sensor(generic_sensor, scope)

    def convert_joint(self, joint: v17.Joint, scope: Scope) -> Scope:
        generic_joint = self._to_generic_joint(joint)
        return super().convert_joint(generic_joint, scope)

    def _to_generic_joint(self, joint: v17.Joint) -> GenericJoint:
        sensors = list()
        for sensor in joint.sensor:
            sensors.append(self._to_generic_sensor(sensor))

        joint_args = {
            "name": joint.name,
            "kind": joint.type,
            "parent": joint.parent,
            "child": joint.child,
            "pose": None,
            "sensor": sensors,
        }

        if joint.pose is not None:
            joint_args["pose"] = joint.pose

        if joint.axis is not None:
            axis = GenericJoint.Axis()

            if joint.axis.xyz is not None:
                axis.xyz.value = joint.axis.xyz.value
                axis.xyz.expressed_in = joint.axis.xyz.expressed_in

            joint_args["axis"] = axis

        return GenericJoint(**joint_args)

    def _to_generic_sensor(self, sensor: v17.Sensor) -> GenericSensor:
        if sensor.pose is None:
            sensor.pose = v17.Sensor.Pose()
        if sensor.camera is not None:
            if sensor.camera.pose is None:
                sensor.camera.pose = v17.Sensor.Camera.Pose()

        return GenericSensor(
            name=sensor.name,
            type=sensor.type,
            pose=GenericPose(
                value=sensor.pose.value, relative_to=sensor.pose.relative_to
            ),
            camera=GenericSensor.Camera(
                name=sensor.camera.name,
                pose=GenericPose(
                    value=sensor.camera.pose.value,
                    relative_to=sensor.camera.pose.relative_to,
                ),
            ),
        )

    def _to_generic_light(self, light: v17.Light) -> GenericLight:
        return GenericLight(name=light.name, pose=light.pose)

    def _to_generic_link(self, link: v17.Link) -> GenericLink:
        link_args = {
            "name": link.name,
            "must_be_base_link": link.must_be_base_link,
            "pose": link.pose,
            "inertial": None,
            "projector": None,
            "sensors": [self._to_generic_sensor(sensor) for sensor in link.sensor],
            "lights": [self._to_generic_light(light) for light in link.light],
        }

        if link.inertial is not None:
            el = PoseBearing(pose=GenericPose(relative_to=link.name))
            if link.inertial.pose is not None:
                el.pose.value = link.inertial.pose.value
                if link.inertial.pose.relative_to is not None:
                    raise NotImplementedError(
                        "Unsure how to resolve intertal/pose/@relative_to."
                    )
            link_args["inertial"] = el

        link_args["collisions"] = [
            NamedPoseBearing(name=c.name, pose=c.pose)
            if c.pose is not None
            else NamedPoseBearing(name=c.name)
            for c in link.collision
        ]

        link_args["visuals"] = [
            NamedPoseBearing(name=v.name, pose=v.pose)
            if v.pose is not None
            else NamedPoseBearing(name=v.name)
            for v in link.visual
        ]

        if link.projector is not None:
            link_args["projector_pose"] = NamedPoseBearing(
                name=link.projector.name, pose=link.projector.pose
            )

        link_args["audio_source_poses"] = [
            a.pose if a.pose is not None else GenericPose() for a in link.audio_source
        ]

        return GenericLink(**link_args)
