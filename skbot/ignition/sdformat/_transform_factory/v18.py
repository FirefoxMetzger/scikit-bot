from typing import List, Union

from .scopes import Scope
from .generic import (
    GenericFrame,
    GenericInclude,
    GenericJoint,
    GenericLink,
    GenericModel,
    GenericPose,
    GenericSensor,
    GenericLight,
    GenericWorld,
    NamedPoseBearing,
    PoseBearing,
)
from .factory import FactoryBase
from .. import sdformat
from ..bindings import v18


IncludeElement = Union[v18.ModelModel.Include, v18.World.Include]
FrameElement = Union[v18.ModelModel.Frame, v18.World.Frame]


class Converter(FactoryBase):
    """Functions to convert v1.8 SDF objects into generic SDF objects."""

    def __call__(self, sdf: str) -> Union[Scope, List[Scope]]:
        """Convert v1.8 SDF into a Scope

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
            generic_world = self._to_generic_world(world)
            graph = self.convert_world(generic_world)
            graph_list.append(graph)

        if sdf_root.model is not None:
            generic_model = self._to_generic_model(sdf_root.model)
            graph = self.convert_model(generic_model)
            graph_list.append(graph)

        if sdf_root.light is not None:
            generic_light = self._to_generic_light(sdf_root.light)
            graph = self.convert_light(generic_light)
            graph_list.append(graph)

        if sdf_root.actor is not None:
            raise NotImplementedError("Actors are not implemented yet.")

        return graph_list

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
        sensor_args = {"name": sensor.name, "type": sensor.type, "pose": sensor.pose}

        if sensor.camera is not None:
            if sensor.camera.noise is not None:
                raise NotImplementedError()
            if sensor.camera.distortion is not None:
                raise NotImplementedError()
            if sensor.camera.lens is not None:
                raise NotImplementedError()

        if sensor.camera is not None:
            sensor_args["camera"] = GenericSensor.Camera(
                name=sensor.camera.name, pose=sensor.camera.pose
            )

        return GenericSensor(**sensor_args)

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
            link_args["inertial"] = GenericLink.Inertial(
                pose=GenericPose(value=link.inertial.pose, relative_to=link.name)
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
            link_args["projector"] = NamedPoseBearing(
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
            frames=[self._to_generic_frame(f) for f in model.frame],
        )

    def _to_generic_frame(self, frame: FrameElement) -> GenericFrame:
        return GenericFrame(
            attached_to=frame.attached_to, name=frame.name, pose=frame.pose
        )

    def _to_generic_include(self, include: IncludeElement) -> GenericInclude:
        return GenericInclude(
            name=include.name,
            pose=include.pose,
            placement_frame=include.placement_frame,
            uri=include.uri,
        )

    def _to_generic_population(
        self, population: v18.World.Population
    ) -> GenericWorld.GenericPopulation:
        distribution = GenericWorld.GenericPopulation.GenericDistribution()
        if population.distribution is not None:
            distribution.type = population.distribution.type
            distribution.step = population.distribution.step
            distribution.cols = population.distribution.cols
            distribution.rows = population.distribution.rows

        return GenericWorld.GenericPopulation(
            name=population.name,
            pose=population.pose,
            model_count=population.model_count,
            distribution=distribution,
            box=population.box,
            cylinder=population.cylinder,
            model=self._to_generic_model(population.model),
        )

    def _to_generic_world(self, world: v18.World) -> GenericWorld:
        return GenericWorld(
            name=world.name,
            includes=[self._to_generic_include(i) for i in world.include],
            models=[self._to_generic_model(m) for m in world.model],
            frames=[self._to_generic_frame(f) for f in world.frame],
            lights=[self._to_generic_light(l) for l in world.light],
            population=[self._to_generic_population(p) for p in world.population],
        )
