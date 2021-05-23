import numpy as np
import ropy.transform as rtf
import pytest


def test_missing_tf_matrix():
    world_frame = rtf.Frame(3)
    camera_frame = rtf.Frame(3)

    link = rtf.affine.Fixed(world_frame, camera_frame, lambda x: x)
    
    with pytest.raises(ValueError):
        rtf.affine.Inverse(link)