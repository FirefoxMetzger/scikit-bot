from dataclasses import dataclass
from .audio_source_type import AudioSourceType


@dataclass
class AudioSource(AudioSourceType):
    """
    An audio source.
    """
    class Meta:
        name = "audio_source"
