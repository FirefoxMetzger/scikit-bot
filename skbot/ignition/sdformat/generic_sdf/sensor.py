import warnings
from typing import List

from .base import ElementBase, NamedPoseBearing, Pose
from .frame import Frame


class Sensor(ElementBase):
  def __init__(self, *, sdf_version: str) -> None:
    warnings.warn("`Sensor` has not been implemented yet.")
    super().__init__(sdf_version=sdf_version)


class Sensor(NamedPoseBearing):
    def __init__(
        self,
        *,
        name: str,
        type: str,
        pose: Pose = None,
        camera: "Camera" = None,
        frames: List["Frame"] = None,
    ) -> None:
        super().__init__(name=name, pose=pose)
        self.type = type
        self.camera = camera
        self.frames = frames

        if frames is None:
            self.frames = list()

    class Camera(NamedPoseBearing):
        def __init__(
            self,
            *,
            name: str,
            pose: Pose = None,
            horizontal_fov: float = 1.047,
            image: "Image" = None,
            frames: "Frame" = None,
        ) -> None:
            super().__init__(name=name, pose=pose)
            self.horizontal_fov = horizontal_fov
            self.image = image
            self.frames = frames

            if self.frames is None:
                self.frames = list()

            if self.image is None:
                self.image = Sensor.Camera.Image()

        class Image:
            def __init__(
                self, *, width: int = 320, height: int = 240, format: str = "R8G8B8"
            ) -> None:
                self.width = width
                self.height = height
                self.format = format




'''<!-- Sensor -->
<element name="sensor" required="0">
  <description>The sensor tag describes the type and properties of a sensor.</description>

  <attribute name="name" type="string" default="__default__" required="1">
    <description>A unique name for the sensor. This name must not match another model in the model.</description>
  </attribute>

  <attribute name="type" type="string" default="__default__" required="1">
    <description>The type name of the sensor. By default, SDFormat supports types
                  air_pressure,
                  altimeter,
                  camera,
                  contact,
                  depth_camera, depth,
                  force_torque,
                  gps,
                  gpu_lidar,
                  gpu_ray,
                  imu,
                  lidar,
                  logical_camera,
                  magnetometer,
                  multicamera,
                  navsat,
                  ray,
                  rfid,
                  rfidtag,
                  rgbd_camera, rgbd,
                  sonar,
                  thermal_camera, thermal,
                  wireless_receiver, and
                  wireless_transmitter.
      The "ray", "gpu_ray", and "gps" types are equivalent to "lidar", "gpu_lidar", and "navsat", respectively. It is preferred to use "lidar", "gpu_lidar", and "navsat" since "ray", "gpu_ray", and "gps" will be deprecated. The "ray", "gpu_ray", and "gps" types are maintained for legacy support.
    </description>
  </attribute>

  <element name="always_on" type="bool" default="false" required="0">
    <description>If true the sensor will always be updated according to the update rate.</description>
  </element>

  <element name="update_rate" type="double" default="0" required="0">
    <description>The frequency at which the sensor data is generated. If left unspecified, the sensor will generate data every cycle.</description>
  </element>

  <element name="visualize" type="bool" default="false" required="0">
    <description>If true, the sensor is visualized in the GUI</description>
  </element>

  <element name="topic" type="string" default="__default__" required="0">
    <description>Name of the topic on which data is published. This is necessary for visualization</description>
  </element>

  <element name="enable_metrics" type="bool" default="false" required="0">
    <description>If true, the sensor will publish performance metrics</description>
  </element>

  <include filename="pose.sdf" required="0"/>
  <include filename="plugin.sdf" required="*"/>
  <include filename="air_pressure.sdf" required="0"/>
  <include filename="altimeter.sdf" required="0"/>
  <include filename="camera.sdf" required="0"/>
  <include filename="contact.sdf" required="0"/>
  <include filename="forcetorque.sdf" required="0"/>
  <include filename="gps.sdf" required="0"/>
  <include filename="imu.sdf" required="0"/>
  <include filename="lidar.sdf" required="0"/>
  <include filename="logical_camera.sdf" required="0"/>
  <include filename="magnetometer.sdf" required="0"/>
  <include filename="navsat.sdf" required="0"/>
  <include filename="ray.sdf" required="0"/>
  <include filename="rfid.sdf" required="0"/>
  <include filename="rfidtag.sdf" required="0"/>
  <include filename="sonar.sdf" required="0"/>
  <include filename="transceiver.sdf" required="0"/>

</element> <!-- End Sensor -->
'''