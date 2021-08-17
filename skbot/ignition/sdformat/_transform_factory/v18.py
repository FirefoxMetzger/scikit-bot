from typing import List, Union

from .scopes import Scope, WorldScope, ModelScope, LightScope
from .links import (
    CustomLink,
    DynamicPose,
    SimplePose,
    RotationJoint,
    PrismaticJoint,
)
from .generic import (
    GenericFrame,
    GenericInclude,
    GenericJoint,
    GenericLink,
    GenericModel,
    GenericPose,
    GenericSensor,
    GenericLight,
    NamedPoseBearing,
    PoseBearing,
)
from .factory import FactoryBase
from .. import sdformat
from ..bindings import v18
from .... import transform as tf
from skbot.ignition.sdformat._transform_factory import scopes


IncludeElement = Union[v18.ModelModel.Include, v18.World.Include]
FrameElement = Union[v18.ModelModel.Frame, v18.World.Frame]


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

    def convert_light(self, light: Union[v18.Light, GenericLight], *, scope: Scope = None) -> Scope:
        if isinstance(light, v18.Light):
            light = self._to_generic_light(light)
        return super().convert_light(self._to_generic_light(light), scope=scope)

    def convert_model(
        self, model: Union[v18.ModelModel, GenericModel], *, parent_scope: Scope = None
    ) -> Scope:
        if isinstance(model, v18.ModelModel):
            model = self._to_generic_model(model)
        return super().convert_model(model, parent_scope=parent_scope)

    def _to_generic_joint(self, joint: v18.Joint) -> GenericJoint:
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

    def _to_generic_sensor(self, sensor: v18.Sensor) -> GenericSensor:
        if sensor.pose is None:
            sensor.pose = v18.Sensor.Pose()
        if sensor.camera is not None:
            if sensor.camera.pose is None:
                sensor.camera.pose = v18.Sensor.Camera.Pose()

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

    def _to_generic_light(self, light: v18.Light) -> GenericLight:
        return GenericLight(name=light.name, pose=light.pose)

    def _to_generic_link(self, link: v18.Link) -> GenericLink:
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
            link_args["inertial_pose"] = PoseBearing(
                value=link.inertial.pose, relative_to=link.name
            )

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

    def _to_generic_model(self, model: v18.ModelModel) -> GenericModel:
        if len(model.gripper) > 0:
            raise NotImplementedError(
                "Gripper not implemented yet (lacking upstream docs)."
            )

        return GenericModel(
            name=model.name,
            pose=model.pose,
            placement_frame=model.placement_frame,
            canonical_link=model.canonical_link,
            links=[self._to_generic_link(l) for l in model.link],
            include=[self._to_generic_include(i) for i in model.include],
            models=[self._to_generic_model(m) for m in model.model],
            joints=[self._to_generic_joint(j) for j in model.joint],
            frames=[self._to_generic_frame(f) for f in model.frame]
        )

    def _to_generic_frame(self, frame: FrameElement) -> GenericFrame:
        return GenericFrame(
            attached_to=frame.attached_to,
            name=frame.name,
            pose=frame.pose
        )

    def _to_generic_include(self, include: IncludeElement) -> GenericInclude:
        return GenericInclude(
            name=include.name,
            pose=include.pose,
            placement_frame=include.placement_frame,
            uri=include.uri,
        )
