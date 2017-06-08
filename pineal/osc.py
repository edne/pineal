from threading import Thread
import liblo
import config

callbacks = {}
sources = {}


def dispatcher(path, args, tags):
    for k in callbacks:
        if k.startswith(path):
            callbacks[k](path, args)


def receive():
    _, port = config.osc_addr
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
