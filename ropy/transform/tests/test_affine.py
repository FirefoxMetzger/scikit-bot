import ropy.transform as rtf
import numpy as np


def test_1d_robot():

    world_frame = rtf.Frame(ndim=2)
    ellbow_frame = rtf.Frame(2)
    tool_frame = rtf.Frame(2)

    joint = rtf.affine.PlanarRotation(ellbow_frame, world_frame, (1, 0), (0, 1))
    ellbow_frame.add_link(joint)
    world_frame.add_link(rtf.affine.Inverse(joint))
    
    arm = rtf.affine.Translation(tool_frame, ellbow_frame, (1, 0))
    tool_frame.add_link(arm)
    ellbow_frame.add_link(rtf.affine.Inverse(arm))

    joint.angle = 0
    tool_pos = tool_frame.transform((0, 0), to_frame=world_frame)
    assert np.allclose(tool_pos, (1, 0))
    
    joint.angle = np.pi/2
    tool_pos = tool_frame.transform((0, 0), to_frame=world_frame)
    assert np.allclose(tool_pos, (0, 1))


def test_fixed_link():
    frame1 = rtf.Frame(3)
    frame2 = rtf.Frame(3)
    frame3 = rtf.Frame(2)

    def flip_projection(x):
        x = np.asarray(x)
        return np.array([-x[2], x[1]])

    frame1.add_link(rtf.affine.Fixed(frame1, frame2, lambda x: np.asarray(x) + 3))
    frame2.add_link(rtf.affine.Fixed(frame2, frame3, flip_projection))
