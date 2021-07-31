from dataclasses import dataclass, field
from typing import List
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
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
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
