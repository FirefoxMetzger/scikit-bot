import warnings

from .base import ElementBase


class ForceTorque(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`ForceTorque` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Contact(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Contact` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Altimeter(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Altimeter` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class AirPressure(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`AirPressure` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Imu(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Imu` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Gps(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Gps` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Magnetometer(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Magnetometer` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class LogicalCamera(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`LogicalCamera` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Navsat(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Navsat` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Rfid(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Rfid` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class RfidTag(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`RfidTag` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Sonar(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Sonar` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Transceiver(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Transceiver` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Ray(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Ray` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Lidar(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`Lidar` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
