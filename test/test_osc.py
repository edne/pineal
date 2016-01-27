from __future__ import print_function
import liblo
from time import sleep


def test_client_server():
    "Test OSC"
    expected = 1234
    checks = [False, False]

    def callback(path, args):
        "Callback"
        print("received message:", path, "with arguments:", args)
        assert args == [expected]
        checks[0] = True

    def fallback(path, args):
        "Fallback callback"
        print("received unknown message:", path, "with arguments:", args)
        checks[1] = True

    server = liblo.ServerThread(7172)
    server.add_method('/foo/message1', 'i', callback)
    server.add_method(None, None, fallback)

    server.start()

    target = liblo.Address(7172)

    liblo.send(target, "/foo/message1", expected)
    liblo.send(target, "/foo/message2", 456.0, "asd")

    sleep(0.1)

    server.stop()

    assert checks[0] and checks[1]
