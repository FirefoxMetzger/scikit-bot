import pytest
import numpy as np
from pathlib import Path

import skbot.ignition as ign


def test_v18_parsing(v18_sdf):    
    ign.transform_graph_from_sdf(v18_sdf)


def test_panda():
    model_file = Path(__file__).parent / "sdf" / "robots" / "panda" / "model.sdf"
    sdf_string = model_file.read_text()

    root_frame = ign.transform_graph_from_sdf(sdf_string)
