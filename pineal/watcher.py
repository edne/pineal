from os.path import abspath
from os.path import split as splitpath
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from atomos.atom import Atom
import logging

log = logging.getLogger(__name__)


code_atom = Atom('')


def add_callback(callback):
    def atom_watch(k, ref, old, new):
        callback(new)

    code_atom.add_watch('file_change', atom_watch)


def make_handler(file_name):
    class Handler(PatternMatchingEventHandler):
        def on_modified(self, event):
            log.debug('Modified: {}'.format(event.src_path))
            with open(file_name) as f:
                code = f.read()
            code_atom.reset(code)

    return Handler(patterns=[abspath(file_name)])


def make_observer(file_name, handler):
    full_path = abspath(file_name)
    folder, _ = splitpath(full_path)

    observer = Observer()
    observer.schedule(handler, folder, False)
    observer.daemon = True
    return observer


def watch(file_name):
    handler = make_handler(file_name)
    observer = make_observer(file_name, handler)

    observer.start()
