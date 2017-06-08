from os.path import abspath
from os.path import split as splitpath
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import liblo
import logging

log = logging.getLogger(__name__)


def send_code(file_name, osc_addr):
    with open(file_name) as f:
        code = f.read()

    liblo.send(osc_addr, '/code', ('s', code))


def make_handler(file_name, osc_addr):
    class Handler(PatternMatchingEventHandler):
        def on_modified(self, event):
            log.debug('Modified: {}'.format(event.src_path))
            send_code(file_name, osc_addr)

    return Handler(patterns=[abspath(file_name)])


def make_observer(file_name, handler):
    full_path = abspath(file_name)
    folder, _ = splitpath(full_path)

    observer = Observer()
    observer.schedule(handler, folder, False)
    observer.daemon = True
    return observer


def watch(file_name, osc_addr):
    handler = make_handler(file_name, osc_addr)
    observer = make_observer(file_name, handler)

    observer.start()
