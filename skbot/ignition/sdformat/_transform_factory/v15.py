from typing import List, Union

from .scopes import Scope
from .factory import FactoryBase
from .. import sdformat
from ..bindings import v15
from .generic import (
    GenericFrame,
    GenericInclude,
    GenericLight,
    GenericModel,
    GenericPose,
    GenericSensor,
    GenericJoint,
    GenericWorld,
    NamedPoseBearing,
    GenericLink,
    PoseBearing,
)


IncludeElement = Union[v15.ModelModel.Include, v15.World.Include]
FrameElement = Union[
    v15.ModelModel.Frame, v15.Sensor.Frame, v15.Joint.Frame, v15.Link.Frame
]
PoseElement = Union[
    v15.ModelModel.Frame.Pose,
    v15.Sensor.Frame.Pose,
    v15.Joint.Frame.Pose,
    v15.Link.Frame.Pose,
    v15.Joint.Pose,
]


class Converter(FactoryBase):
    """Functions to convert v1.5 SDF objects into generic SDF objects."""

    def __call__(self, sdf: str) -> Union[Scope, List[Scope]]:
        """Convert v1.5 SDF into a Scope"""

        sdf_root: v15.Sdf = sdformat.loads(sdf)
        graph_list: List[Scope] = list()

        for world in sdf_root.world:
            generic_world = self._to_generic_world(world)
            graph = self.convert_world(generic_world)
            graph_list.append(graph)

        for model in sdf_root.model:
            generic_model = self._to_generic_model(model)
            graph = self.convert_model(generic_model)
            graph_list.append(graph)

        for light in sdf_root.light:
            generic_light = self._to_generic_light(light)
            graph = self.convert_light(generic_light)
            graph_list.append(graph)

        return graph_list

    def _to_generic_pose(self, pose: PoseElement) -> GenericPose:
        if pose is None:
            return GenericPose()
        else:
            return GenericPose(value=pose.value, relative_to=pose.frame)

    def _to_generic_frame(self, frame: FrameElement, attached_to=None) -> GenericFrame:
        return GenericFrame(
            attached_to=attached_to,
            name=frame.name,
            pose=self._to_generic_pose(frame.pose),
        )

    def _to_generic_sensor(self, sensor: v15.Sensor) -> GenericSensor:
        sensor_args = {
            "name": sensor.name,
            "type": sensor.type,
            "pose": self._to_generic_pose(sensor.pose),
            "frames": [
                self._to_generic_frame(x, attached_to=None) for x in sensor.frame
            ],
        }

        if sensor.camera is not None:
            if sensor.camera.noise is not None:
                raise NotImplementedError()
            if sensor.camera.distortion is not None:
                raise NotImplementedError()
            if sensor.camera.lens is not None:
                raise NotImplementedError()

            sensor_args["camera"] = GenericSensor.Camera(
                name=sensor.camera.name,
                pose=self._to_generic_pose(sensor.camera.pose),
                horizontal_fov=sensor.camera.horizontal_fov,
                frames=[
                    self._to_generic_frame(x, attached_to=None)
                    for x in sensor.camera.frame
                ],
            )

            if sensor.camera.image is not None:
                sensor_args["camera"].image = GenericSensor.Camera.Image(
                    width=sensor.camera.image.width,
                    height=sensor.camera.image.height,
                    format=sensor.camera.image.format,
                )

        return GenericSensor(**sensor_args)

    def _to_generic_joint(self, joint: v15.Joint) -> GenericJoint:
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
            "frames": [
                self._to_generic_frame(x, attached_to=joint.name) for x in joint.frame
            ],
        }

        if joint.pose is not None:
            joint_args["pose"] = GenericPose(
                value=joint.pose.value, relative_to=joint.pose.frame
            )

        if joint.axis is not None:
            axis = GenericJoint.Axis()

            axis.xyz.value = joint.axis.xyz
            if not joint.axis.use_parent_model_frame:
                axis.xyz.expressed_in = joint.child
            else:
                axis.xyz.expressed_in = joint.parent

            if joint.axis.limit is not None:
                axis.limit.lower = joint.axis.limit.lower
                axis.limit.upper = joint.axis.limit.upper
                axis.limit.effort = joint.axis.limit.effort
                axis.limit.velocity = joint.axis.limit.velocity
                axis.limit.stiffness = joint.axis.limit.stiffness
                axis.limit.dissipation = joint.axis.limit.dissipation

            joint_args["axis"] = axis

        return GenericJoint(**joint_args)

    def _to_generic_light(self, light: v15.Light) -> GenericLight:
        return GenericLight(
            name=light.name,
            frames=[
                self._to_generic_frame(x, attached_to=light.name) for x in light.frame
            ],
            pose=self._to_generic_pose(light.pose),
        )

    def _to_generic_link(self, link: v15.Link) -> GenericLink:
        link_args = {
            "name": link.name,
            "must_be_base_link": link.must_be_base_link,
            "pose": self._to_generic_pose(link.pose),
            "inertial": None,
            "projector": None,
            "sensors": [self._to_generic_sensor(sensor) for sensor in link.sensor],
            "frames": [
                self._to_generic_frame(f, attached_to=link.name) for f in link.frame
            ]
            # lights may not be part of SDF 1.5; tracking issue:
            #
            # "lights": [self._to_generic_light(light) for light in link.light],
        }

        if link.inertial is not None:
            el = GenericLink.Inertial(
                pose=GenericPose(relative_to=link.name),
                frames=[self._to_generic_frame(f) for f in link.inertial.frame],
            )
            if link.inertial.pose is not None:
                el.pose.value = link.inertial.pose.value
                if link.inertial.pose.frame is not None:
                    raise NotImplementedError(
                        "Unsure how to resolve /inertial/pose/@frame."
                    )
            link_args["inertial"] = el

        link_args["collisions"] = [
            NamedPoseBearing(name=c.name, pose=self._to_generic_pose(c.pose))
            if c.pose is not None
            else NamedPoseBearing(name=c.name)
            for c in link.collision
        ]

        link_args["visuals"] = [
            NamedPoseBearing(name=v.name, pose=self._to_generic_pose(v.pose))
            if v.pose is not None
            else NamedPoseBearing(name=v.name)
            for v in link.visual
        ]

        if link.projector is not None:
            link_args["projector"] = NamedPoseBearing(
                name=link.projector.name,
                pose=self._to_generic_pose(link.projector.pose),
            )

        link_args["audio_source_poses"] = [
            self._to_generic_pose(a.pose) if a.pose is not None else GenericPose()
            for a in link.audio_source
        ]

        return GenericLink(**link_args)

    def _to_generic_include(self, include: IncludeElement) -> GenericInclude:
        return GenericInclude(
            name=include.name,
            pose=self._to_generic_pose(include.pose),
            uri=include.uri,
        )

    def _to_generic_model(self, model: v15.ModelModel) -> GenericModel:
        if len(model.gripper) > 0:
            raise NotImplementedError(
                "Gripper not implemented yet (lacking upstream docs)."
            )

        return GenericModel(
            name=model.name,
            include=[self._to_generic_include(i) for i in model.include],
            models=[self._to_generic_model(m) for m in model.model],
            frames=[
                self._to_generic_frame(f, attached_to="__model__") for f in model.frame
            ],
            pose=self._to_generic_pose(model.pose),
            links=[self._to_generic_link(l) for l in model.link],
            joints=[self._to_generic_joint(j) for j in model.joint],
        )

    def _to_generic_population(
        self, population: v15.World.Population
    ) -> GenericWorld.GenericPopulation:
        distribution = GenericWorld.GenericPopulation.GenericDistribution()
        if population.distribution is not None:
            distribution.type = population.distribution.type
            distribution.step = population.distribution.step
            distribution.cols = population.distribution.cols
            distribution.rows = population.distribution.rows

        generic_population = GenericWorld.GenericPopulation(
            name=population.name,
            pose=self._to_generic_pose(population.pose),
            model_count=population.model_count,
            distribution=distribution,
            model=self._to_generic_model(population.model),
            frames=[self._to_generic_frame(x) for x in population.frame],
        )

        if population.box is not None:
            generic_population.box = GenericWorld.GenericPopulation.GenericBox(
                size=population.box.size
            )

        if population.cylinder is not None:
            generic_population.cylinder = (
                GenericWorld.GenericPopulation.GenericCylinder(
                    radius=population.cylinder.radius, length=population.cylinder.length
                )
            )

        return generic_population

    def _to_generic_world(self, world: v15.World) -> GenericWorld:
        return GenericWorld(
            name=world.name,
            includes=[self._to_generic_include(i) for i in world.include],
            models=[self._to_generic_model(m) for m in world.model],
            frames=list(),
            lights=[self._to_generic_light(l) for l in world.light],
            population=[self._to_generic_population(p) for p in world.population],
        )
