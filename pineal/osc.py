import liblo
import config

callbacks = {}
sources = {}


def dispatcher(path, args, tags):
    for k in callbacks:
        if k.startswith(path):
            callbacks[k](path, args)


def osc_receiver():
    _, port = config.osc_addr
    server = liblo.ServerThread(port)
    server.add_method(None, None, dispatcher)
    return server.start


start_server = osc_receiver()


def add_callback(key, cb):
    callbacks[key] = cb
