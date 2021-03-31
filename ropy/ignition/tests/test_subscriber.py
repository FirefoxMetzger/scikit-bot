import ropy.ignition as ign
import subprocess
import time
import psutil
import pytest


@pytest.fixture
def ign_instance():
    """Start a gazebo instance to test subscription"""

    gazebo = subprocess.Popen(["ign", "gazebo", "shapes.sdf", "-s"])

    # wait for gazebo to start
    time.sleep(3)

    yield

    pobj = psutil.Process(gazebo.pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()
    gazebo.terminate()


def test_subscriber_raw(ign_instance):
    with ign.Subscriber("/clock") as clock:
        msg = clock.recv()

    assert msg.sim.sec == 0 and msg.sim.nsec == 0


def test_subscriber_parse(ign_instance):
    def parse_clock(msg):
        return ign.messages.Clock().parse(msg[2])

    with ign.Subscriber("/clock", parser=parse_clock) as clock:
        msg = clock.recv()

    assert msg.sim.sec == 0 and msg.sim.nsec == 0


def test_subscriber_noblock(ign_instance):
    with pytest.raises(IOError):
        with ign.Subscriber("/clock") as clock:
            msg = clock.recv(blocking=False)


def test_subscriber_address_error():
    with pytest.raises(IOError):
        with ign.Subscriber("/clock") as clock:
            msg = clock.recv()
