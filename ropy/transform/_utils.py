import numpy as np
from math import sqrt, atan
from numpy.typing import ArrayLike


def vector_project(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    """ Returns the component of a along b.
    """

    a = np.asarray(a)
    b = np.asarray(b)

    return np.dot(a,b) / np.dot(b, b) * b


def angle_between(a: ArrayLike, b: ArrayLike) -> float:
    """ Computes the signed angle from a to b

    Notes
    -----
    Implementation is based on this StackOverflow post:
    https://scicomp.stackexchange.com/a/27694
    """

    a = np.asarray(a)
    b = np.asarray(b)

    c = np.linalg.norm(a - b)
    a = np.linalg.norm(a)
    b = np.linalg.norm(b)

    if a >= b:
        flipped = 1
    else:
        flipped = -1
        a,b = b, a

    if c > b:
        mu = b - (a-c)
    else:
        mu = c - (a-b)

    numerator = ((a - b) + c)*mu
    denominator = (a + (b + c))*((a-c)+b)
    angle = 2*atan(sqrt(numerator/denominator))

    return flipped * angle