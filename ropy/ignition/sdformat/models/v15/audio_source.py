from dataclasses import dataclass
from .audio_source_type import AudioSourceType


@dataclass
class AudioSource(AudioSourceType):
    class Meta:
        name = "audio_source"
