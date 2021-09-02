import zmq
import subprocess
import socket
import os
import getpass

from . import messages


class Subscriber:
    """Subscribe and listen to Ignition messages.

    Ignition uses ZMQ_ to pass around protocol buffers as means of
    communication. This subscriber enabels python to receive copies of these
    buffers. For more information on the messages published by ignition, and how
    it works, check out the `Ign-Msgs documentation`_ as well as the
    `Ign-Transport documentation`_.


    .. _ZMQ: https://zeromq.org/
    .. _`Ign-Msgs documentation`: https://ignitionrobotics.org/api/msgs/6.4/index.html
    .. _`Ign-Transport documentation`: https://ignitionrobotics.org/api/transport/9.1/index.html
    """

    def __init__(self, topic: str, *, parser=None):
        """Initialize a new subscriber for the given topic.

        Creates an object that uses a context manager to subscribe to
        ign-transport topics and receive messages from it.

        Parameters
        ----------
        topic : str
            The name of the topic to subscribe to as shown by `ign topic -l`.
        parser : function
            A function that deserializes the message. The signature of the parser function
            is ``fn(zmq_message) -> result`` where zmq_message is a 3-tuple of the form
            (zmq_topic, protobuf_message, message_type). If None, the subscriber
            will use a default parser that converts ``protobuf_message`` into a
            ``skbot.ignition.message.<message_type>`` data object.

        Returns
        -------
        self : Subscriber
            A object that can subscribe to ign-transport within a context
            manager

        """
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.topic = topic

        # this could be streamlined by speaking the ign-transport discovery protcol
        host_name = socket.gethostname()
        user_name = getpass.getuser()
        self.socket.subscribe(f"@/{host_name}:{user_name}@{topic}")

        if parser is None:
            self.parser = lambda msg: getattr(
                messages, msg[3].decode("utf-8").split(".")[-1]
            )().parse(msg[2])
        else:
            self.parser = parser

    def recv(self, blocking=True, timeout=1000) -> tuple:
        """Receive a message from the topic

        Parameters
        ----------
        blocking : bool
            If True (default) block until a message is received. If False, raise
            zmq.ZMQError if no message is available at the time of query.
        timeout : int
            Time (in ms) to wait for a message to arrive. If the time is
            exceeded, an IOError will be raised. Will wait indefinitely if set
            to `-1`. This only works if ``blocking=True``.

        Returns
        -------
        msg : PyObject
            If a parser was specified during instantiation, returns the result
            of the parser. Otherwise it will use the default parser and return a
            ``skbot.ignition.messages.<message_type>`` data object.
        """

        self.socket.setsockopt(zmq.RCVTIMEO, timeout)

        try:
            if blocking:
                msg = self.socket.recv_multipart()
            else:
                msg = self.socket.recv_multipart(zmq.NOBLOCK)
        except zmq.Again:
            raise IOError(f"Topic {self.topic} did not send a message.")

        result = self.parser(msg)

        return result

    def __enter__(self):
        # weird hack to encourage ign-transport to actually publish camera
        # messages start an echo subscriber and print the messages into the void
        # to make ign realize that something is listening to the topic tracking
        # issue: https://github.com/ignitionrobotics/ign-transport/issues/225
        self.echo_subscriber = subprocess.Popen(
            ["ign", "topic", "-e", "-t", self.topic], stdout=open(os.devnull, "w")
        )

        # this is a bad hack and should be implemented by talking the
        # ign-transport discovery protocol
        result = subprocess.check_output(f"ign topic -i -t {self.topic}", shell=True)
        self.address = (
            result.decode("utf-8")
            .split("\n")[1]
            .split(",")[0]
            .replace("\t", "")
            .replace(" ", "")
        )

        if not self.address:
            self.echo_subscriber.terminate()
            raise IOError(f"Could not identify socket for {self.topic}.")

        self.socket.connect(self.address)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.disconnect(self.address)
        self.echo_subscriber.terminate()
