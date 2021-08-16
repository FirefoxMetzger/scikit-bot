from typing import List, Union

from .graph import (
    CustomLink,
    Scope,
    DynamicPose,
    SimplePose,
    RotationJoint,
    PrismaticJoint,
    ModelScope,
    WorldScope,
)
from .factory import ConverterBase
from .. import sdformat
from ..bindings import v18
from .... import transform as tf


IncludeElement = Union[v18.ModelModel.Include, v18.World.Include]


class Converter(ConverterBase):
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

        sdf_root: v18.Sdf = sdformat.loads(sdf)
        graph_list: List[Scope] = list()

        for world in sdf_root.world:
            graph = self.convert_world(world)
            graph_list.append(graph)

        if sdf_root.model is not None:
            graph = self.convert_model(sdf_root.model)
            graph_list.append(graph)

        if sdf_root.light is not None:
            graph = self.convert_light(sdf_root.light)
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

        if include.placement_frame is not None:
            placement_frame = include.placement_frame
        else:
            placement_frame = subscope.placement_frame
            #TODO: deal with absend //include/pose
            # not quite sure how yet.

        if include.pose.relative_to is None:
            include.pose.relative_to = name

        placement_frame = subscope.name + "::" + placement_frame

        scope.add_scaffold(
            placement_frame, include.pose.value, include.pose.relative_to
        )

        child = subscope.name + "::" + subscope.cannonical_link
        scope.declare_link(DynamicPose(name, child))

    def convert_world(self, world: v18.World) -> Scope:
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
                frame.pose = v18.World.Frame.Pose()

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

    def convert_state(self, state: v18.State) -> Scope:
        raise NotImplementedError()

    def convert_light(self, light: v18.Light, *, scope: Scope = None) -> Scope:
        if scope is None:
            scope = Scope()

        if light.pose is None:
            light.pose = v18.Light.Pose()

        scope.declare_frame(light.name)
        scope.add_scaffold(light.name, light.pose.value, light.pose.relative_to)

        return scope

    def convert_actor(self) -> Scope:
        raise NotImplementedError()

    def convert_model(
        self, model: v18.ModelModel, *, parent_scope: Scope = None
    ) -> Scope:
        scope = ModelScope(
            model.name,
            placement_frame=model.placement_frame,
            canonical_link=model.canonical_link,
        )

        if model.pose is None:
            model.pose = v18.ModelModel.Pose()

        for link in model.link:
            if scope.cannonical_link is None:
                scope.cannonical_link = link.name

            self.convert_link(link, scope)

        for include in model.include:
            self.resolve_include(include, scope)

        for nested_model in model.model:
            self.convert_model(nested_model, parent_scope=scope)

            # double-check if this is correct
            scope.add_scaffold(nested_model.name, "0 0 0 0 0 0")
            scope.declare_link(SimplePose(scope.default_frame, nested_model.name, "0 0 0 0 0 0"))

        for frame in model.frame:
            if frame.pose is None:
                frame.pose = v18.ModelModel.Frame.Pose()

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

    def convert_link(self, link: v18.Link, scope: Scope) -> Scope:
        if link.must_be_base_link:
            link.pose.relative_to = "world"
            scope.declare_link(DynamicPose("world", link.name))

        if link.pose is None:
            link.pose = v18.Link.Pose()

        scope.declare_frame(link.name)
        scope.add_scaffold(link.name, link.pose.value, link.pose.relative_to)

        if link.inertial:
            scope.declare_link(
                SimplePose(link.name, tf.Frame(3, name="inertial"), link.inertial.pose)
            )

        for collision in link.collision:
            if collision.pose is None:
                collision.pose = v18.Collision.Pose()

            scope.declare_frame(collision.name)
            scope.add_scaffold(
                collision.name, collision.pose.value, collision.pose.relative_to
            )
            scope.declare_link(DynamicPose(link.name, collision.name))

        for visual in link.visual:
            if visual.pose is None:
                visual.pose = v18.Visual.Pose()

            scope.declare_frame(visual.name)
            scope.add_scaffold(visual.name, visual.pose.value, visual.pose.relative_to)
            scope.declare_link(DynamicPose(link.name, visual.name))

        for sensor in link.sensor:
            self.convert_sensor(sensor, scope)
            scope.declare_link(DynamicPose(link.name, sensor.name))

        if link.projector:
            if link.projector.pose is None:
                link.projector.pose = v18.Link.Projector.Pose()

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

        for idx, source in enumerate(link.audio_source):
            if source.pose is None:
                source.pose = v18.Link.AudioSource.Pose()

            name = link.name + f"-audio-source-{idx}"
            scope.declare_frame(name)
            scope.add_scaffold(name, source.pose.value, source.pose.relative_to)
            scope.declare_link(DynamicPose(link.name, name))

        for light in link.light:
            self.convert_light(light, scope=scope)
            scope.declare_link(DynamicPose(link.name, light.name))

        return scope

    def convert_sensor(self, sensor: v18.Sensor, scope: Scope) -> Scope:
        if sensor.pose is None:
            sensor.pose = v18.Sensor.Pose()

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

    def convert_joint(self, joint: v18.Joint, scope: Scope) -> Scope:
        if joint.pose is None:
            joint.pose = v18.Joint.Pose()

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
