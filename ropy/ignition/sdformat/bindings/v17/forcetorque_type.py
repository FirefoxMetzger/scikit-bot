from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "sdformat/forcetorque"


@dataclass
class ForceTorqueType:
    """
    These elements are specific to the force torque sensor.

    Parameters
    ----------
    frame: Frame in which to report the wrench values. Currently
        supported frames are: "parent" report the wrench expressed in
        the orientation of the parent link frame, "child" report the
        wrench expressed in the orientation of the child link frame,
        "sensor" report the wrench expressed in the orientation of the
        joint sensor frame. Note that for each option the point with
        respect to which the torque component of the wrench is expressed
        is the joint origin.
    measure_direction: Direction of the wrench measured by the sensor.
        The supported options are: "parent_to_child" if the measured
        wrench is the one applied by the parent link on the child link,
        "child_to_parent" if the measured wrench is the one applied by
        the child link on the parent link.
    """

    class Meta:
        name = "force_torqueType"

    frame: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    measure_direction: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
