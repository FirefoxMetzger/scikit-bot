from dataclasses import dataclass, field
from typing import List, Optional
from .material_type import MaterialType
from .pose_type import PoseType

__NAMESPACE__ = "sdformat/particle_emitter"


@dataclass
class ParticleEmitterType:
    """
    A particle emitter that can be used to describe fog, smoke, and dust.

    Parameters
    ----------
    emitting: True indicates that the particle emitter should generate
        particles when loaded
    duration: The number of seconds the emitter is active. A value less
        than or equal to zero means infinite duration.
    size: The size of the emitter where the particles are sampled.
        Default value is (1, 1, 1). Note that the interpretation of the
        emitter area varies depending on the emmiter type: - point: The
        area is ignored. - box: The area is interpreted as width X
        height X depth. - cylinder: The area is interpreted as the
        bounding box of the cylinder. The cylinder is oriented along the
        Z-axis. - ellipsoid: The area is interpreted as the bounding box
        of an ellipsoid shaped area, i.e. a sphere or squashed-sphere
        area. The parameters are again identical to EM_BOX, except that
        the dimensions describe the widest points along each of the
        axes.
    particle_size: The particle dimensions (width, height, depth).
    lifetime: The number of seconds each particle will ’live’ for before
        being destroyed. This value must be greater than zero.
    rate: The number of particles per second that should be emitted.
    min_velocity: Sets a minimum velocity for each particle (m/s).
    max_velocity: Sets a maximum velocity for each particle (m/s).
    scale_rate: Sets the amount by which to scale the particles in both
        x and y direction per second.
    color_start: Sets the starting color for all particles emitted. The
        actual color will be interpolated between this color and the one
        set under color_end. Color::White is the default color for the
        particles unless a specific function is used. To specify a
        color, RGB values should be passed in. For example, to specify
        red, a user should enter:
    color_end: Sets the end color for all particles emitted. The actual
        color will be interpolated between this color and the one set
        under color_start. Color::White is the default color for the
        particles unless a specific function is used (see color_start
        for more information about defining custom colors with RGB
        values). Note that this function overrides the particle colors
        set with color_range_image.
    color_range_image: Sets the path to the color image used as an
        affector. This affector modifies the color of particles in
        flight. The colors are taken from a specified image file. The
        range of color values begins from the left side of the image and
        moves to the right over the lifetime of the particle, therefore
        only the horizontal dimension of the image is used.  Note that
        this function overrides the particle colors set with color_start
        and color_end.
    topic: Topic used to update particle emitter properties at runtime.
        The default topic is
        /model/{model_name}/particle_emitter/{emitter_name} Note that
        the emitter id and name may not be changed.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect to the frame named in the relative_to attribute.
    material: The material of the visual element.
    name: A unique name for the particle emitter.
    type: The type of a particle emitter. One of "box", "cylinder",
        "ellipsoid", or "point".
    """

    class Meta:
        name = "particle_emitterType"

    emitting: List[bool] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    duration: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    size: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    particle_size: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    lifetime: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    rate: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    min_velocity: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    max_velocity: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    scale_rate: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    color_start: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    color_end: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    color_range_image: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    topic: List[str] = field(
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
    material: List[MaterialType] = field(
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
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
