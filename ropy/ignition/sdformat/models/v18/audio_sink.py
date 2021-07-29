from dataclasses import dataclass
from .audio_sink_type import AudioSinkType


@dataclass
class AudioSink(AudioSinkType):
    """
    An audio sink.
    """
    class Meta:
        name = "audio_sink"
