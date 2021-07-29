from dataclasses import dataclass
from .particle_emitter_type import ParticleEmitterType


@dataclass
class ParticleEmitter(ParticleEmitterType):
    """
    A particle emitter that can be used to describe fog, smoke, and dust.
    """
    class Meta:
        name = "particle_emitter"
