from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/gripper"


@dataclass
class GripperType:
    class Meta:
        name = "gripperType"

    grasp_check: List["GripperType.GraspCheck"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gripper_link: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    palm_link: List[str] = field(
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

    @dataclass
    class GraspCheck:
        detach_steps: List[int] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        attach_steps: List[int] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        min_contact_count: List[int] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
