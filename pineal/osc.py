from threading import Thread
import liblo

callbacks = {}
sources = {}


def dispatcher(path, args, tags):
    for k in callbacks:
        if k.startswith(path):
            callbacks[k](path, args)


def receive(port):
    server = liblo.Server(port)
    server.add_method(None, None, dispatcher)
    # return server.start

    def recv():
        while True:
            server.recv()

    t = Thread(target=recv)
    t.daemon = True
    t.start()


def add_callback(key, cb):
    callbacks[key] = cb
