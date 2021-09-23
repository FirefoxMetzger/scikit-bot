import warnings

from .base import ElementBase


class AudioSink(ElementBase):
    def __init__(self, *, sdf_version: str) -> None:
        warnings.warn("`AudioSink` has not been implemented yet.")
        super().__init__(sdf_version=sdf_version)


"""<!-- Audio Sink -->
<element name="audio_sink" required="*">
  <description>An audio sink.</description>
</element>
"""
