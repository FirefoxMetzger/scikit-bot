import skbot.ignition as ign
import subprocess
import time
import psutil
import pytest
import shutil


HAS_IGN = False if shutil.which("ign") is None else True


@pytest.fixture
def ign_instance():
    """Start a gazebo instance to test subscription"""

    gazebo = subprocess.Popen(["ign", "gazebo", "shapes.sdf", "-s"])

    # wait for gazebo to start
    time.sleep(7)

    yield

    pobj = psutil.Process(gazebo.pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()
    gazebo.terminate()


@pytest.mark.skipif(not HAS_IGN, reason="Ignition executable not found.")
def test_subscriber_raw(ign_instance):
    with ign.Subscriber("/clock") as clock:
        msg = clock.recv()

    assert msg.sim.sec == 0 and msg.sim.nsec == 0


@pytest.mark.skipif(not HAS_IGN, reason="Ignition executable not found.")
def test_subscriber_parse(ign_instance):
    def parse_clock(msg):
        return ign.messages.Clock().parse(msg[2])

    with ign.Subscriber("/clock", parser=parse_clock) as clock:
        msg = clock.recv()

    assert msg.sim.sec == 0 and msg.sim.nsec == 0


@pytest.mark.skipif(not HAS_IGN, reason="Ignition executable not found.")
def test_subscriber_noblock(ign_instance):
    with pytest.raises(IOError):
        with ign.Subscriber("/clock") as clock:
            msg = clock.recv(blocking=False)


@pytest.mark.skipif(not HAS_IGN, reason="Ignition executable not found.")
def test_subscriber_address_error():
    with pytest.raises(IOError):
        with ign.Subscriber("/clock") as clock:
            msg = clock.recv()
