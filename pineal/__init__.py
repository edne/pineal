import logging
from .graphic.renderer import render
from .watcher import watch
from .listener import listen

# TODO: read loglevel and audio input/channels from config file
logging.basicConfig(level=logging.DEBUG)

_running = []


def run(file_name):
    if file_name and file_name not in _running:
        _running.append(file_name)

        listen('default', 2)  # listen for audio input
        watch(file_name)

        try:
            render(file_name)  # blocking
        except KeyboardInterrupt:
            print()
