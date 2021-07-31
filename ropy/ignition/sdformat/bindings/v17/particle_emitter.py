from dataclasses import dataclass
from .particle_emitter_type import ParticleEmitterType


@dataclass
class ParticleEmitter(ParticleEmitterType):
    class Meta:
        name = "particle_emitter"
