from os.path import abspath
from os.path import split as splitpath
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import liblo
import config
import logging

log = logging.getLogger(__name__)


def coder():
    def new_handler(file_name):
        def get_code():
            with open(file_name) as f:
                return f.read()

        def is_valid(path):
            return abspath(path) == abspath(file_name)

        liblo.send(config.OSC_EYE, '/eye/code', ('s', get_code()))

        class Handler(FileSystemEventHandler):
            def on_modified(self, event):
                path = event.src_path
                if abspath(path) == abspath(file_name):
                    liblo.send(config.OSC_EYE, '/eye/code',
                               ('s', get_code()))

        return Handler()

    observer = Observer()
    file_name = config.file_name

    full_path = abspath(file_name)
    folder, _ = splitpath(full_path)

    observer.schedule(new_handler(file_name), folder, False)
    observer.start()  # Maybe run() ?

    while True:
        sleep(1000)

    observer.stop()
    observer.join()
