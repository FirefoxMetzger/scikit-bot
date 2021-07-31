from dataclasses import dataclass, field
from typing import List, Optional

__NAMESPACE__ = "sdformat/noise"


@dataclass
class NoiseType:
    """
    The properties of a sensor noise model.

    Parameters
    ----------
    mean: For type "gaussian*", the mean of the Gaussian distribution
        from which noise values are drawn.
    stddev: For type "gaussian*", the standard deviation of the Gaussian
        distribution from which noise values are drawn.
    bias_mean: For type "gaussian*", the mean of the Gaussian
        distribution from which bias values are drawn.
    bias_stddev: For type "gaussian*", the standard deviation of the
        Gaussian distribution from which bias values are drawn.
    precision: For type "gaussian_quantized", the precision of output
        signals. A value of zero implies infinite precision / no
        quantization.
    type: The type of noise. Currently supported types are: "none" (no
        noise). "gaussian" (draw noise values independently for each
        measurement from a Gaussian distribution). "gaussian_quantized"
        ("gaussian" plus quantization of outputs (ie. rounding))
    """
    class Meta:
        name = "noiseType"

    mean: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    stddev: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    bias_mean: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    bias_stddev: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    precision: List[float] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
