#!/usr/bin/env python
from __future__ import print_function
import os
from sys import argv

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import hy
from pineal.utils import hy_eval_string


def watch(file_name):
    "Return a watchdog observer"

    def on_modified(event):
        "File-changed event"
        if event.src_path == file_name:
            print("changed")

    handler = FileSystemEventHandler()
    handler.on_modified = on_modified
    observer = Observer()

    base_path = os.path.split(file_name)[0]
    observer.schedule(handler, path=base_path)
    observer.start()

    return observer


def main(file_name):
    "Main function"

    ns = {}  # namespace

    with open(file_name) as f:
        hy_eval_string(f.read(), ns)

    from time import sleep
    observer = watch(file_name)
    try:
        while True:
            ns["loop"]()
            sleep(1.0/120)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    if argv[1:]:
        main(argv[1])
    else:
        print("Usage: ", argv[0], "filename")
