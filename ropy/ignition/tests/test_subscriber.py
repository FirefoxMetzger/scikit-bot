import ropy.ignition as ign
import subprocess
import time
import psutil


def test_subscriber():
    gazebo = subprocess.Popen(["ign", "gazebo", "shapes.sdf", "-r", "-s"])

    with ign.Subscriber("/clock") as clock:
        msg = clock.recv()

    assert msg is not None

    pobj = psutil.Process(gazebo.pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()
