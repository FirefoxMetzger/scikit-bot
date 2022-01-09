import warnings

from .base import ElementBase, should_warn_unsupported


class ForceTorque(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`ForceTorque` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Contact(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Contact` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Altimeter(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Altimeter` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class AirPressure(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`AirPressure` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Imu(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Imu` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Gps(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Gps` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Magnetometer(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Magnetometer` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class LogicalCamera(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`LogicalCamera` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Navsat(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Navsat` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Rfid(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Rfid` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class RfidTag(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`RfidTag` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Sonar(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Sonar` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Transceiver(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Transceiver` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Ray(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Ray` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


class Lidar(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        if should_warn_unsupported():
            warnings.warn("`Lidar` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)
