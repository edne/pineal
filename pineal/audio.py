import numpy as np
import jack


def hear(callback, channels=2, body=None,
         jack_client="Hear",
         rate=44100, frames_per_buffer=1024):

    def default_body():
        from time import sleep
        try:
            while True:
                sleep(0.1)
        except KeyboardInterrupt:
            print("\nInterrupted by user")

    if body is None:
        body = default_body

    client = jack.Client(jack_client)

    if client.status.server_started:
        print("JACK server started")
    if client.status.name_not_unique:
        print("unique name {0!r} assigned".format(client.name))

    @client.set_process_callback
    def process(frames):
        assert len(client.inports) == channels
        assert frames == client.blocksize

        data = [np.fromstring(channel.get_buffer(),
                              dtype=np.float32)
                for channel in client.inports]

        callback(data)

    for i in range(channels):
        client.inports.register("input_{0}".format(i+1))

    client.activate()
    capture = client.get_ports(is_physical=True, is_output=True)

    if capture:
        for src, dest in zip(capture, client.inports):
            try:
                client.connect(src, dest)
            except jack.JackError:
                pass

    body()

    client.deactivate()
    client.close()
