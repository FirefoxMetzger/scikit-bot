from dataclasses import dataclass, field
from typing import List
from .frame_type import FrameType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/audio_source"


@dataclass
class AudioSourceType:
    """
    An audio source.

    Parameters
    ----------
    uri: URI of the audio media.
    pitch: Pitch for the audio media, in Hz
    gain: Gain for the audio media, in dB.
    contact: List of collision objects that will trigger audio playback.
    loop: True to make the audio source loop playback.
    frame: A frame of reference to which a pose is relative.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the specified frame.
    """

    class Meta:
        name = "audio_sourceType"

    uri: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pitch: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gain: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    contact: List["AudioSourceType.Contact"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    loop: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    frame: List[FrameType] = field(
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

    @dataclass
    class Contact:
        """
        List of collision objects that will trigger audio playback.

        Parameters
        ----------
        collision: Name of child collision element that will trigger
            audio playback.
        """

        collision: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
