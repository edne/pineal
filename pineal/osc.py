import liblo
from atomos.atomic import AtomicFloat
import config

callbacks = {}
sources = {}


def dispatcher(path, args, tags):
    for k in callbacks:
        if k.startswith(path):
            callbacks[k](path, args)


def osc_receiver():
    server = liblo.ServerThread(config.OSC_EYE[1])
    server.add_method(None, None, dispatcher)
    return server.start


start_server = osc_receiver()


def add_callback(key, cb):
    callbacks[key] = cb


def get_source(name):
    if name not in sources:
        container = AtomicFloat()

        def set_value(path, values):
            container.set(values[0])

        add_callback(name, set_value)
        sources[name] = container.get

    return sources[name]
