#!/usr/bin/env python
from __future__ import print_function
import os
from sys import argv
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import liblo

logger = logging.getLogger("watcher.py")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def watch_file(file_name, action, *args, **kwargs):
    "Return a watchdog observer, it will call the action callback"
    def on_modified(event):
        "File-changed event"
        if not os.path.exists(event.src_path):
            return

        logger.info("Changed %s" % event.src_path)

        if os.path.samefile(event.src_path, file_name):
            action(*args, **kwargs)

    logger.info("Started watcher")

    handler = FileSystemEventHandler()
    handler.on_modified = on_modified
    observer = Observer()

    base_path = os.path.split(file_name)[0]
    if not base_path:
        base_path = "."

    observer.schedule(handler, path=base_path)
    observer.start()

    return observer


def check_address(addr):
    "If only port is specified send to localhost"
    splitted = str(addr).split(":")
    if splitted[1:]:
        return addr
    else:
        return ":".join(["localhost", splitted[0]])


def send(addr, path, *msg):
    """address path message
    Send message on a given path"""
    addr = check_address(addr)
    target = liblo.Address("osc.udp://" + addr + "/")
    liblo.send(target, path, *msg)


def main():
    "Main function"
    if len(argv) != 4:
        print("Watch a file for changes and send it via OSC")
        print("Usage:", argv[0], "file_to_watch [ip:]port /path")
        return

    file_name, addr, path = argv[1:]

    def callback():
        with open(file_name) as f:
            logger.info("Sending content")
            send(addr, path, f.read())

    watcher = watch_file(file_name, callback)
    callback()
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        watcher.stop()
    watcher.join()

if __name__ == "__main__":
    main()
