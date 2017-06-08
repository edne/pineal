from os.path import abspath
from os.path import split as splitpath
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import liblo
import logging
import config

log = logging.getLogger(__name__)


def send_code():
    file_name = config.file_name
    osc_addr = config.osc_addr

    with open(file_name) as f:
        code = f.read()

    liblo.send(osc_addr, '/code', ('s', code))


class Handler(PatternMatchingEventHandler):
    def on_modified(self, event):
        log.debug('Modified: {}'.format(event.src_path))
        send_code()


def watch():
    send_code()

    file_name = config.file_name
    full_path = abspath(file_name)
    folder, _ = splitpath(full_path)

    handler = Handler(patterns=[full_path])

    observer = Observer()
    observer.schedule(handler, folder, False)
    observer.daemon = True
    observer.start()
