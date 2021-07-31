from dataclasses import dataclass

__NAMESPACE__ = "sdformat/audio_sink"


@dataclass
class AudioSinkType:
    """
    An audio sink.
    """

    class Meta:
        name = "audio_sinkType"
