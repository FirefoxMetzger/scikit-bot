from skbot.ignition.messages import Pose
from skbot.ignition.sdformat.bindings.v17 import light
from typing import List


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
    def __init__(self, *, name:str, pose: GenericPose = None) -> None:
        super().__init__(pose=pose)
        self.name = name


class GenericSensor(PoseBearing):
    def __init__(
        self, *, name: str, type: str, pose: GenericPose = None, camera: "Camera" = None
    ) -> None:
        super().__init__(pose=pose)
        self.type = type
        self.camera = camera
        self.name = name

    class Camera(PoseBearing):
        def __init__(
            self,
            *,
            name: str,
            pose: GenericPose = None,
            horizontal_fov: float = 1.047,
            image: "Image" = None,
        ) -> None:
            super().__init__(pose=pose)
            self.horizontal_fov = horizontal_fov
            self.image = image
            self.name = name

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
    ) -> None:
        super().__init__(pose=pose)
        self.name = name
        self.type = kind
        self.parent = parent
        self.child = child
        self.axis = axis
        self.sensor = sensor

        if axis is None:
            self.axis = GenericJoint.Axis()

        if self.axis.xyz.expressed_in is None:
            self.axis.xyz.expressed_in = self.child

    class Axis:
        def __init__(self, *, xyz: "GenericJoint.Axis.Xyz" = None) -> None:
            self.xyz = xyz
            if xyz is None:
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
        inertial: PoseBearing = None,
        collisions: List[NamedPoseBearing],
        visuals: List[NamedPoseBearing],
        projector: NamedPoseBearing = None,
        audio_source_poses: List[GenericPose],
        sensors: List[GenericSensor],
        lights: List["GenericLight"]
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

        if audio_source_poses is None:
            audio_source_poses = list()
        self.audio_sources = [PoseBearing(pose=p) for p in audio_source_poses]


class GenericLight(NamedPoseBearing):
    pass