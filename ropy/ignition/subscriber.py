import zmq
import subprocess
import socket
import os
import pwd

class IgnSubscriber:
    def __init__(self, topic: str, *, parser = None):
        """
        Initialize a new subscriber for the given topic.

        Creates an object that uses a context manager to subscribe to
        ign-transport topics and receive messages from it.

        Parameters
        ----------
        topic : str
            The name of the topic to subscribe to as shown by `ign topic -l`.
        parser : function
            A function that deserializes the message. If None, the raw message
            will be returned.
        
        Returns
        -------
        self : IgnSubscriber
            A object that can subscribe to ign-transport within a context
            manager

        """
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.topic = topic

        self.parser = parser

        # this could be streamlined by speaking the ign-transport discovery protcol
        host_name = socket.gethostname()
        user_name = pwd.getpwuid(os.getuid())[0]
        self.socket.subscribe(f"@/{host_name}:{user_name}@{topic}")

    def recv(self, blocking=True, timeout=1000) -> tuple:
        """
        Receive a message from the topic

        Parameters
        ----------
        blocking : bool
            If True (default) block until a message is received. If False, raise
            zmq.ZMQError if no message is available at the time of query.
        timeout : int
            Time (in ms) to wait for a message to arrive. If the time is
            exceeded, an IOError will be raised. Will wait indefinitely if set
            to `-1`.

        Returns
        -------
        msg : Tuple
            The received message.
        """

        self.socket.setsockopt(zmq.RCVTIMEO, timeout)

        try:
            if blocking:
                msg = self.socket.recv_multipart()
            else:
                msg = self.socket.recv_multipart(zmq.NOBLOCK)
        except zmq.Again:
            raise IOError(f"Topic {self.topic} did not send a message.")

        if self.parser is not None:
            msg = self.parser(msg)

        return msg

    def __enter__(self):
        # weird hack to encourage ign-transport to actually publish camera
        # messages start an echo subscriber and print the messages into the void
        # to make ign realize that something is listening to the topic tracking
        # issue: https://github.com/ignitionrobotics/ign-transport/issues/225
        self.echo_subscriber = subprocess.Popen(
            ["ign", "topic", "-e", "-t", self.topic], 
            stdout=open(os.devnull, 'w')
        )

        # this is a bad hack and should be implemented by talking the
        # ign-transport discovery protocol
        result = subprocess.check_output(f"ign topic -i -t {self.topic}", shell=True)
        self.address = result.decode("utf-8").split("\n")[1].split(",")[0].replace("\t", "").replace(" ", "")

        if not self.address:
            self.echo_subscriber.terminate()
            raise IOError(f"Could not identify socket for {self.topic}.")

        self.socket.connect(self.address)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.disconnect(self.address)
        self.echo_subscriber.terminate()
