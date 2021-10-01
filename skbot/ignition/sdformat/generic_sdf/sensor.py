import warnings
from typing import List, Any, Dict, Tuple
from itertools import chain

from .base import (
    BoolElement,
    ElementBase,
    FloatElement,
    NamedPoseBearing,
    Pose,
    StringElement,
)
from .frame import Frame
from .origin import Origin
from .plugin import Plugin
from .camera import Camera
from .ray import Ray
from .contact import Contact
from .rfid import RfidTag
from .rfidtag import Rfid
from .imu import Imu
from .forcetorque import ForceTorque
from .gps import Gps
from .sonar import Sonar
from .transceiver import Transceiver
from .altimeter import Altimeter
from .logical_camera import LogicalCamera
from .magnetometer import Magnetometer
from .air_pressure import AirPressure
from .lidar import Lidar
from .navsat import Navsat
from .... import transform as tf


class Sensor(ElementBase):
    """A sensor.

    Parameters
    ----------
    name : str
        A unique name for the sensor. This name must not match another sensor
        under the same parent.
    type : str
        The type name of the sensor. The "ray", "gpu_ray", and "gps" types are
        equivalent to "lidar", "gpu_lidar", and "navsat", respectively. It is
        preferred to use "lidar", "gpu_lidar", and "navsat" since "ray",
        "gpu_ray", and "gps" will be deprecated. The "ray", "gpu_ray", and "gps"
        types are maintained for legacy support. Must be one of:
            - air_pressure
            - altimeter
            - camera
            - contact
            - depth_camera, depth
            - force_torque
            - gps
            - gpu_lidar
            - gpu_ray
            - imu
            - lidar
            - logical_camera
            - magnetometer
            - multicamera
            - navsat
            - ray
            - rfid
            - rfidtag
            - rgbd_camera, rgbd
            - sonar
            - thermal_camera, thermal
            - wireless_receiver
            - wireless_transmitter
    always_on : bool
        If true the sensor will always be updated according to the update rate.
        Default is ``False``.
    update_rate : float
        The frequency at which the sensor data is generated. If set to 0, the
        sensor will generate data every cycle. Default is ``0``.
    visualize : bool
        If true, the sensor is visualized in the GUI. Default is ``False``.
    enable_metrics : bool
        If true, the sensor will publish performance metrics. Default is ``False``.

        .. versionadded:: SDFormat v1.7
    pose : Pose
        The links's initial position (x,y,z) and orientation (roll, pitch, yaw).

        .. versionadded:: SDFormat 1.2
    topic : str
        Name of the topic on which data is published.
    plugins : List[Plugin]
        A list of plugins used to customize the runtime behavior of the
        simulation.
    air_pressure : AirPressure
        Parameters of a Barometer sensor.

        .. versionadded:: SDFormat v1.6
    camera : Camera
        Parameters of a Camera sensor.
    ray : Ray
        Parameters of a Laser sensor.
    contact : Contact
        Parameters of a Contact sensor.
    rfid : Rfid
        Parameters of a RFID sensor.
    rfidtag : RfidTag
        Parameters of a RFID Tag.
    imu : Imu
        Parameters of a Inertial Measurement Unit (IMU).

        .. versionadded:: SDFormat v1.3
    force_torque : ForceTorque
        Parameters of a torque sensor.

        .. versionadded:: SDFormat v1.4
    gps : Gps
        Parameters of a GPS.

        .. versionadded:: SDFormat v1.4
    sonar : Sonar
        parameters of a Sonar.

        .. versionadded:: SDFormat v1.4
    transceiver : Transceiver
        Parameters for a wireless transceiver.

        .. versionadded:: SDFormat v1.4
    altimeter : Altimeter
        Parameters for an Altimeter,

        .. versionadded:: SDFormat v1.5
    lidar : Lidar
        Parameters of a LIDAR sensor.

        .. versionadded:: SDFormat v1.6
    logical_camera : LogicalCamera
        Parameters of a logical camera.
    magnetometer : Magnetometer
        Parameters of a magnetometer.

        .. versionadded:: SDFormat v1.5
    navsat : Navsat
        Parameters of a GPS.

        .. versionadded:: SDFormat v1.7
    sdf_version : str
        The SDFormat version to use when constructing this element.
    origin : Origin
        The link's origin.

        .. deprecated:: SDFormat v1.2
            Use `Sensor.pose` instead.
    frames : List[Frame]
        A list of frames of reference in which poses may be expressed.

        .. deprecated:: SDFormat v1.7
            Use :attr:`Model.frame` instead.
        .. versionadded:: SDFormat v1.5

    Attributes
    ----------
    particle_emitters : List[ParticleEmitter]
        See ``Parameters`` section.
    name : str
        See ``Parameters`` section.
    type : str
        See ``Parameters`` section.
    always_on : bool
        See ``Parameters`` section.
    update_rate : float
        See ``Parameters`` section.
    visualize : bool
        See ``Parameters`` section.
    enable_metrics : bool
        See ``Parameters`` section.
    pose : Pose
        See ``Parameters`` section.
    topic : str
        See ``Parameters`` section.
    plugins : List[Plugin]
        See ``Parameters`` section.
    air_pressure : AirPressure
        See ``Parameters`` section.
    camera : Camera
        See ``Parameters`` section.
    ray : Ray
        See ``Parameters`` section.
    contact : Contact
        See ``Parameters`` section.
    rfid : Rfid
        See ``Parameters`` section.
    rfidtag : RfidTag
        See ``Parameters`` section.
    imu : Imu
        See ``Parameters`` section.
    force_torque : ForceTorque
        See ``Parameters`` section.
    gps : Gps
        See ``Parameters`` section.
    sonar : Sonar
        See ``Parameters`` section.
    transceiver : Transceiver
        See ``Parameters`` section.
    altimeter : Altimeter
        See ``Parameters`` section.
    lidar : Lidar
        See ``Parameters`` section.
    logical_camera : LogicalCamera
        See ``Parameters`` section.
    magnetometer : Magnetometer
        See ``Parameters`` section.
    navsat : Navsat
        See ``Parameters`` section.

    """

    def __init__(
        self,
        *,
        name: str,
        type: str,
        always_on: bool = False,
        update_rate: float = 0,
        visualize: bool = False,
        enable_metrics: bool = False,
        origin: Origin = None,
        pose: Pose = None,
        topic: str = None,
        plugins: List[Plugin],
        air_pressure: AirPressure = None,
        camera: Camera = None,
        ray: Ray = None,
        contact: Contact = None,
        rfid: Rfid = None,
        rfidtag: RfidTag = None,
        imu: Imu = None,
        force_torque: ForceTorque = None,
        gps: Gps = None,
        sonar: Sonar = None,
        transceiver: Transceiver = None,
        frames: List[Frame] = None,
        altimeter: Altimeter = None,
        lidar: Lidar = None,
        logical_camera: LogicalCamera = None,
        magnetometer: Magnetometer = None,
        navsat: Navsat = None,
        sdf_version: str,
    ) -> None:
        super().__init__(sdf_version=sdf_version)

        self.name = name
        self.type = type
        self.always_on = always_on
        self.update_rate = update_rate
        self.visualize = visualize
        self.enable_metrics = enable_metrics
        if origin is None:
            self._origin = Origin(sdf_version=sdf_version)
        elif sdf_version == "1.0":
            self._origin = origin
        else:
            warnings.warn("`origin` is deprecated. Use `Sensor.pose` instead.")
            self._origin = origin
        if sdf_version == "1.0":
            self.pose = self._origin.pose
        elif pose is None:
            self.pose = Pose(sdf_version=sdf_version)
        else:
            self.pose = pose
        self.topic = self.type if topic is None else topic
        self.plugins = [] if plugins is None else plugins
        self.air_pressure = (
            AirPressure(sdf_version=sdf_version)
            if air_pressure is None
            else air_pressure
        )
        self.camera = Camera(sdf_version=sdf_version) if camera is None else camera
        self.ray = Ray(sdf_version=sdf_version) if ray is None else ray
        self.contact = Contact(sdf_version=sdf_version) if contact is None else contact
        self.rfid = Rfid(sdf_version=sdf_version) if rfid is None else rfid
        self.rfidtag = RfidTag(sdf_version=sdf_version) if rfidtag is None else rfidtag
        self.imu = Imu(sdf_version=sdf_version) if imu is None else imu
        self.force_torque = (
            ForceTorque(sdf_version=sdf_version)
            if force_torque is None
            else force_torque
        )
        self.gps = Gps(sdf_version=sdf_version) if gps is None else gps
        self.sonar = Sonar(sdf_version=sdf_version) if sonar is None else sonar
        self.transceiver = (
            Transceiver(sdf_version=sdf_version) if transceiver is None else transceiver
        )
        self._frames = [] if frames is None else frames
        self.altimeter = (
            Altimeter(sdf_version=sdf_version) if altimeter is None else altimeter
        )
        self.lidar = Lidar(sdf_version=sdf_version) if lidar is None else lidar
        self.logical_camera = (
            LogicalCamera(sdf_version=sdf_version)
            if logical_camera is None
            else logical_camera
        )
        self.magnetometer = (
            Magnetometer(sdf_version=sdf_version)
            if magnetometer is None
            else magnetometer
        )
        self.navsat = Navsat(sdf_version=sdf_version) if navsat is None else navsat

        self._origin.pose = self.pose

    @property
    def origin(self):
        warnings.warn(
            "`Sensor.origin` is deprecated since SDFormat v1.2. Use `Sensor.pose` instead."
        )
        return self._origin

    @property
    def frames(self):
        warnings.warn(
            "`Sensor.frames` is deprecated since SDF v1.7."
            " Use `Model.frames` instead and set `Frame.attached_to` to the name of this link.",
            DeprecationWarning,
        )
        return self._frames

    @classmethod
    def from_specific(cls, specific: Any, *, version: str) -> "ElementBase":
        sensor_args = {
            "name": specific.name,
            "type": specific.type,
        }
        args_with_default = {
            "always_on": BoolElement,
            "update_rate": FloatElement,
            "visualize": BoolElement,
            "enable_metrics": BoolElement,
            "origin": Origin,
            "pose": Pose,
            "topic": StringElement,
            "air_pressure": AirPressure,
            "camera": Camera,
            "ray": Ray,
            "contact": Contact,
            "rfid": Rfid,
            "rfidtag": RfidTag,
            "imu": Imu,
            "force_torque": ForceTorque,
            "gps": Gps,
            "sonar": Sonar,
            "transceiver": Transceiver,
            "altimeter": Altimeter,
            "lidar": Lidar,
            "logical_camera": LogicalCamera,
            "magnetometer": Magnetometer,
            "navsat": Navsat,
        }
        list_args = {
            "plugin": ("plugins", Plugin),
            "frame": ("frames", Frame),
        }
        standard_args = cls._prepare_standard_args(
            specific, args_with_default, list_args, version=version
        )
        sensor_args.update(standard_args)
        return Sensor(**sensor_args, sdf_version=version)

    def declared_frames(self) -> Dict[str, tf.Frame]:
        declared_frames = {self.name: tf.Frame(3, name=self.name)}

        relevant_config = None
        if self.type == "camera":
            relevant_config = self.camera
        else:
            warnings.warn(f"Sensor type `{self.type}` is not implemented.")

        if relevant_config is not None:
            nested_elements = relevant_config.declared_frames()
            for name, frame in nested_elements.items():
                declared_frames[f"{self.name}::{name}"] = frame

        for frame in self._frames:
            for name, frame in frame.declared_frames().items():
                declared_frames[f"{self.name}::{name}"] = frame

        return declared_frames

    def to_static_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        sensor_frame: str,
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
    ) -> tf.Frame:
        self.pose.to_static_graph(declared_frames, sensor_frame, shape=shape, axis=axis)

        relevant_config = None
        if self.type == "camera":
            relevant_config = self.camera
        else:
            warnings.warn(f"Sensor type `{self.type}` is not implemented.")

        if relevant_config is not None:
            relevant_config.to_static_graph(
                declared_frames,
                sensor_frame,
                seed=seed,
                shape=shape,
                axis=axis,
            )

        for frame in self._frames:
            frame.pose.to_static_graph(
                declared_frames, f"{sensor_frame}::{frame.name}", shape=shape, axis=axis
            )

        return declared_frames[sensor_frame]

    def to_dynamic_graph(
        self,
        declared_frames: Dict[str, tf.Frame],
        sensor_frame: str,
        *,
        seed: int = None,
        shape: Tuple,
        axis: int = -1,
        apply_state: bool = True,
        _scaffolding: Dict[str, tf.Frame],
    ) -> tf.Frame:
        relevant_config = None
        if self.type == "camera":
            relevant_config = self.camera
        else:
            warnings.warn(f"Sensor type `{self.type}` is not implemented.")

        if relevant_config is not None:
            relevant_config.to_dynamic_graph(
                declared_frames,
                sensor_frame,
                seed=seed,
                shape=shape,
                axis=axis,
                apply_state=apply_state,
                _scaffolding=_scaffolding,
            )

        return declared_frames[sensor_frame]
