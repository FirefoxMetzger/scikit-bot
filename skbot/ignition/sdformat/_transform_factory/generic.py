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


class GenericSensor(PoseBearing):
    def __init__(
        self, *, type: str, pose: GenericPose = None, camera: "Camera" = None
    ) -> None:
        super().__init__(pose=pose)
        self.type = type
        self.camera = camera

    class Camera(PoseBearing):
        def __init__(
            self,
            *,
            name: str,
            pose: GenericPose = None,
            horizontal_fov: float = 1.047,
            image: "Image" = None
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
        type: str,
        parent: str,
        child: str,
        axis: "Axis",
        pose: GenericPose = None,
        sensor: List[GenericSensor] = None
    ) -> None:
        super().__init__(pose=pose)
        self.type = type
        self.parent = str
        self.child = str
        self.axis = axis
        self.sensor = sensor

    class Axis:
        def __init__(self, *, value: str = "0 0 1", expressed_in) -> None:
            self.value = value
            self.expressed_in = expressed_in

