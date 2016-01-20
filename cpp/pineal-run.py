#!/usr/bin/env python
from __future__ import print_function
import os
from time import sleep
from sys import argv
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import hy
from pineal.hy_utils import run_hy_code

logger = logging.getLogger("pineal-run")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def run_code(ns, history):
    "Run last code in the history, if available"
    if history:
        try:
            run_hy_code(history[-1], ns)
        except Exception as e:
            logger.info("Error evaluating code")
            logger.error(e)
            history.pop()
            run_code(ns, history)
    else:
        logger.error("Empty history, there is no valid code")


def update_file(file_name, ns, history):
    "Update running code, saving in the history"
    logger.info("Updating file")

    with open(file_name) as f:
        code = f.read()

    history.append(code)
    run_code(ns, history)


def watch_file(file_name, action, *args, **kwargs):
    "Return a watchdog observer, it will call the action callback"

    def on_modified(event):
        "File-changed event"
        logger.info(file_name, " changed")
        if event.src_path == file_name:
            action(file_name, *args, **kwargs)

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
    history = []  # handle old versions of code

    update_file(file_name, ns, history)

    watcher = watch_file(file_name, update_file, ns, history)
    try:
        while True:
            try:
                ns["loop"]()
            except Exception as e:
                logger.error(e)
                history.pop()
                run_code(ns, history)
            sleep(1.0/120)
    except KeyboardInterrupt:
        watcher.stop()

    watcher.join()

if __name__ == "__main__":
    if argv[1:]:
        main(argv[1])
    else:
        print("Usage: ", argv[0], "filename")
