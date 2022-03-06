""" 

Working with a Hexagonal Grid
=============================

This example showcases one of the more esoteric features of scikit-bot's
transformation library: transformation to and from hexagonal coordinate systems. 

Why would you want to use hexagonal coordinates? Various reasons: Firstly, they
are useful in imaging applications, because they provide better sampling
efficiency than their square-shaped alternative. Secondly, they are useful for
occupancy grids because neighbouring elements have the same distance from each
other. Finally, they look really cool and make for nice visualizations in a
paper.

"""

import numpy as np
import skbot.transform as tf
import matplotlib.pyplot as plt
import matplotlib

cmap = matplotlib.cm.get_cmap("tab10")

# %%
# There is two parts to using them: Firstly there is
# :class:`tf.AxialHexagonTransform <skbot.transform.AxialHexagonTransform>`,
# which transforms 2D cartesian coordinates into hexagonal coordinates. Here are
# a few examples::
#
#    tf.AxialHexagonTransform()
#    tf.AxialHexagonTransform(size=4)  # a hex grid with larger hexagons
#    tf.AxialHexagonTransform(flat_top=False)  # a hex grid that is rotated by 90 degrees
#
# When you use this transformation, the result will be a continous value, which
# is useful because it keeps all information and can be inverted to go back to
# cartesian coordinates. However, often you want to know which hexagon a
# coordinate falls into, which is where :class:`tf.HexagonAxisRound
# <skbot.transform.HexagonAxisRound>` comes in. As the name suggests, it will
# round a vector in hexagon coordinates to the closest hexagon.
#
# We can use this, for example, to perform rejection sampling on the hexagon grid:

to_hex = tf.AxialHexagonTransform()
from_hex = tf.InvertLink(to_hex)

# a 3x3 hex grid (because we can use a nice colormap in this case)
grid = np.stack(np.meshgrid(np.arange(3), np.arange(3)), axis=-1)
hex_centers = from_hex.transform(grid)

sampling_rectangle = [-1, -1, 7, 5]
x, y, w, h = [-1, -1, 7, 5]
candidate_points = np.random.rand(150, 2) * (h, w) + (y, x)
hex_points = to_hex.transform(candidate_points)
hex_points_rounded = tf.HexagonAxisRound().transform(hex_points)
is_in_hexagon = np.all(np.isin(hex_points_rounded, [0, 1, 2]), axis=1)
points = candidate_points[is_in_hexagon, :]  # points are rejected here

# %%
# We can also use :class:`tf.HexagonAxisRound
# <skbot.transform.HexagonAxisRound>` to figure out which hexagon a sampled
# point fell into, and then use that information to label the sampled point:

hex_points = to_hex.transform(points)
hex_points_rounded = tf.HexagonAxisRound().transform(hex_points)
col_idx = np.ravel_multi_index(tuple(hex_points_rounded[:, ::-1].T), (3, 3))

plt.scatter(points[..., 1], points[..., 0], marker="s", c=cmap(col_idx))
plt.scatter(hex_centers[..., 1], hex_centers[..., 0], c=cmap(np.arange(9)), s=150)
for pos in hex_centers.reshape(-1, 2):
    patch = matplotlib.patches.RegularPolygon(
        (pos[1], pos[0]), numVertices=6, radius=1, alpha=0.2, edgecolor="k"
    )
    plt.gca().add_patch(patch)
