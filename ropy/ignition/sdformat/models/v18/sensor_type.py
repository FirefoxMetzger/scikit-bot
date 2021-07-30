from dataclasses import dataclass, field
from typing import List, Optional
from .air_pressure_type import AirPressureType
from .altimeter_type import AltimeterType
from .camera_type import CameraType
from .contact_type import ContactType
from .forcetorque_type import ForceTorqueType
from .gps_type import GpsType
from .imu_type import ImuType
from .lidar_type import LidarType
from .logical_camera_type import LogicalCameraType
from .magnetometer_type import MagnetometerType
from .plugin_type import PluginType
from .pose_type import PoseType
from .ray_type import RayType
from .rfid_type import RfidtagType
from .rfidtag_type import RfidType
from .sonar_type import SonarType
from .transceiver_type import TransceiverType

__NAMESPACE__ = "sdformat/sensor"


@dataclass
class SensorType:
    """
    Parameters
    ----------
    always_on: If true the sensor will always be updated according to
        the update rate.
    update_rate: The frequency at which the sensor data is generated. If
        left unspecified, the sensor will generate data every cycle.
    visualize: If true, the sensor is visualized in the GUI
    topic: Name of the topic on which data is published. This is
        necessary for visualization
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    air_pressure: These elements are specific to an air pressure sensor.
    altimeter: These elements are specific to an altimeter sensor.
    camera: These elements are specific to camera sensors.
    contact: These elements are specific to the contact sensor.
    force_torque: These elements are specific to the force torque
        sensor.
    gps: These elements are specific to the GPS sensor.
    imu: These elements are specific to the IMU sensor.
    lidar: These elements are specific to the lidar sensor.
    logical_camera: These elements are specific to logical camera
        sensors. A logical camera reports objects that fall within a
        frustum. Computation should be performed on the CPU.
    magnetometer: These elements are specific to a Magnetometer sensor.
    ray: These elements are specific to the ray (laser) sensor.
    rfidtag:
    rfid:
    sonar: These elements are specific to the sonar sensor.
    transceiver: These elements are specific to a wireless transceiver.
    name: A unique name for the sensor. This name must not match another
        model in the model.
    type: The type name of the sensor. By default, SDFormat supports
        types air_pressure, altimeter, camera, contact, depth_camera,
        depth, force_torque, gps, gpu_lidar, gpu_ray, imu, lidar,
        logical_camera, magnetometer, multicamera, ray, rfid, rfidtag,
        rgbd_camera, rgbd, sonar, thermal_camera, thermal,
        wireless_receiver, and wireless_transmitter. The "ray" and
        "gpu_ray" types are equivalent to "lidar" and "gpu_lidar",
        respectively. It is preferred to use "lidar" and "gpu_lidar"
        since "ray" and "gpu_ray" will be deprecated. The "ray" and
        "gpu_ray" types are maintained for legacy support.
    """

    class Meta:
        name = "sensorType"

    always_on: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    update_rate: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    visualize: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    topic: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: List[PoseType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    plugin: List[PluginType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    air_pressure: List[AirPressureType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    altimeter: List[AltimeterType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    camera: List[CameraType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    contact: List[ContactType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    force_torque: List[ForceTorqueType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gps: List[GpsType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    imu: List[ImuType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    lidar: List[LidarType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    logical_camera: List[LogicalCameraType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    magnetometer: List[MagnetometerType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    ray: List[RayType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    rfidtag: List[RfidtagType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    rfid: List[RfidType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    sonar: List[SonarType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    transceiver: List[TransceiverType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
