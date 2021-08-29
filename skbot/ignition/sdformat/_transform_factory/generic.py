""" Generic Bindings for SDFormat

The classes below are a poor man's version of the data bindings in
sdformat.bindings. They only implement a subset of the full SDFormat spec
relevant to frame graphs, but are independent of any specific version.

The idea is that a converter for a specific SDF version takes SDF objects of that
version and converts them into the generic representation below. The generic
objects are then used to construct the actual frame graph.
"""


from typing import List, Tuple


class GenericPose:
    def __init__(self, *, value: str = "0 0 0 0 0 0", relative_to: str = None) -> None:
        self.value = value
        self.relative_to = relative_to


class PoseBearing:
    def __init__(self, *, pose: GenericPose = None) -> None:
        self.pose = pose
        if self.pose is None:
            self.pose = GenericPose()


class NamedPoseBearing(PoseBearing):
    def __init__(self, *, name: str, pose: GenericPose = None) -> None:
        super().__init__(pose=pose)
        self.name = name


class GenericSensor(PoseBearing):
    def __init__(
        self,
        *,
        name: str,
        type: str,
        pose: GenericPose = None,
        camera: "Camera" = None,
        frames: List["GenericFrame"] = None,
    ) -> None:
        super().__init__(pose=pose)
        self.type = type
        self.camera = camera
        self.name = name
        self.frames = frames

        if frames is None:
            self.frames = list()

    class Camera(PoseBearing):
        def __init__(
            self,
            *,
            name: str,
            pose: GenericPose = None,
            horizontal_fov: float = 1.047,
            image: "Image" = None,
            frames: "GenericFrame" = None,
        ) -> None:
            super().__init__(pose=pose)
            self.horizontal_fov = horizontal_fov
            self.image = image
            self.name = name
            self.frames = frames

            if self.frames is None:
                self.frames = list()

            if self.image is None:
                self.image = GenericSensor.Camera.Image()

        class Image:
            def __init__(
                self, *, width: int = 320, height: int = 240, format: str = "R8G8B8"
            ) -> None:
                self.width = width
                self.height = height
                self.format = format


class GenericJoint(PoseBearing):
    def __init__(
        self,
        *,
        name: str,
        kind: str,
        parent: str,
        child: str,
        axis: "Axis" = None,
        pose: GenericPose = None,
        sensor: List[GenericSensor] = None,
        frames: List["GenericFrame"] = None,
    ) -> None:
        super().__init__(pose=pose)
        self.name = name
        self.type = kind
        self.parent = parent
        self.child = child
        self.axis = axis
        self.sensor = sensor
        self.frames = frames

        if axis is None:
            self.axis = GenericJoint.Axis()

        if self.axis.xyz.expressed_in is None:
            self.axis.xyz.expressed_in = self.child

        if frames is None:
            self.frames = list()

    class Axis:
        def __init__(self) -> None:
            self.xyz = GenericJoint.Axis.Xyz()

        class Xyz:
            def __init__(self, *, value: str = "0 0 1", expressed_in=None) -> None:
                self.value = value
                self.expressed_in = expressed_in


class GenericLink(PoseBearing):
    def __init__(
        self,
        *,
        name: str,
        pose: GenericPose = None,
        must_be_base_link: bool = False,
        inertial: "GenericLink.Inertial" = None,
        collisions: List[NamedPoseBearing],
        visuals: List[NamedPoseBearing],
        projector: NamedPoseBearing = None,
        audio_source_poses: List[GenericPose],
        sensors: List[GenericSensor],
        lights: List["GenericLight"] = None,
        frames: List["GenericFrame"] = None,
    ) -> None:
        super().__init__(pose=pose)
        self.must_be_base_link = must_be_base_link
        self.name = name
        self.inertial = inertial
        self.projector = projector
        self.collision = collisions
        self.visual = visuals
        self.sensors = sensors
        self.lights = lights
        self.audio_sources = [PoseBearing(pose=p) for p in audio_source_poses]
        self.frames = frames

        if frames is None:
            self.frames = list()

        if lights is None:
            self.lights = list()

    class Inertial(PoseBearing):
        def __init__(
            self, *, pose: GenericPose = None, frames: List["GenericFrame"] = None
        ) -> None:
            super().__init__(pose=pose)
            self.frames = frames

            if self.frames is None:
                self.frames = list()


class GenericLight(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        pose: GenericPose = None,
        frames: List["GenericFrame"] = None,
    ) -> None:
        super().__init__(name=name, pose=pose)

        self.frames = frames

        if frames is None:
            self.frames = list()


class GenericInclude(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        pose: GenericPose = None,
        placement_frame: str = None,
        uri: str,
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.placement_frame = placement_frame
        self.uri = uri
        if pose is None:
            # here pose is None means no overwrite
            self.pose = None


class GenericFrame(NamedPoseBearing):
    def __init__(
        self, *, name: str, pose: GenericPose, attached_to: str = None
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.attached_to = attached_to


class GenericModel(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        pose: GenericPose = None,
        placement_frame: str = None,
        canonical_link: str = None,
        links: List[GenericLink],
        include: List[GenericInclude],
        models: List["GenericModel"],
        frames: List[GenericFrame],
        joints: List[GenericJoint],
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.placement_frame = placement_frame
        self.canonical_link = canonical_link
        self.links = links
        self.include = include
        self.models = models
        self.frames = frames
        self.joints = joints

        if self.canonical_link is None:
            if len(links) > 0:
                self.canonical_link = links[0].name
            elif len(include) > 0:
                self.canonical_link = include[0].name
            elif len(models) > 0:
                self.canonical_link = models[0].name

        if self.placement_frame is None:
            self.placement_frame = "__model__"

        for frame in self.frames:
            if frame.attached_to is None:
                frame.attached_to = self.placement_frame
            elif frame.attached_to == "":
                frame.attached_to = self.placement_frame


class GenericWorld:
    def __init__(
        self,
        *,
        name: str,
        includes: List[GenericInclude],
        lights: List[GenericLight],
        frames: List[GenericFrame],
        models: List[GenericModel],
        population: List["GenericPopulation"],
    ) -> None:
        self.name = name
        self.includes = includes
        self.lights = lights
        self.frames = frames
        self.models = models
        self.population = population

    class GenericPopulation(NamedPoseBearing):
        def __init__(
            self,
            *,
            name: str,
            pose: GenericPose = None,
            model_count: int = 1,
            distribution: "GenericDistribution",
            box: "GenericBox" = None,
            cylinder: "GenericCylinder" = None,
            model: GenericModel,
            frames: List[GenericFrame] = None,
        ) -> None:
            super().__init__(name=name, pose=pose)
            self.model_count = model_count
            self.distribution = distribution
            self.box = box
            self.cylinder = cylinder
            self.model = model
            self.frames = frames

            if frames is None:
                self.frames = list()

        class GenericDistribution:
            def __init__(
                self,
                *,
                kind: str = "random",
                rows: int = 1,
                cols: int = 1,
                step: Tuple[float] = (0.5, 0.5, 0),
            ):
                self.type = kind
                self.rows = rows
                self.cols = cols
                self.step = step

        class GenericBox:
            def __init__(self, *, size: Tuple[float] = (1, 1, 1)) -> None:
                self.size = size

        class GenericCylinder:
            def __init__(self, *, radius: float = 1, length: float = 1) -> None:
                self.radius = radius
                self.length = length
