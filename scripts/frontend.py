#!/usr/bin/env python
from __future__ import print_function
import os
from sys import argv
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import liblo

logger = logging.getLogger("frontend.py")
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


def osc_send(addr, path, *msg):
    "Send message on a given path"
    logger.info("Sending {0} {1}".format(path, msg))

    addr = check_address(addr)
    target = liblo.Address("osc.udp://" + addr + "/")
    liblo.send(target, path, *msg)


def main():
    "Main function"
    if len(argv) < 2:
        print("Watch a file for changes and send to pineal server")
        print("Usage:", argv[0], "file_to_watch [server_addr] [listen_port]")
        return

    file_name = argv[1]
    server_addr = argv[2] if argv[2:] else "127.0.0.1:7172"
    listen_port = argv[3] if argv[3:] else 7173
    listen_port = int(listen_port)

    def update_code():
        with open(file_name) as f:
            logger.info("Sending content")
            osc_send(server_addr, "/run-code", f.read())

    state = {}
    state["server-responding"] = False

    def osc_handle(path, msg):
        if path == "/ack":
            logger.info("/ack received, sending code")
            state["server-responding"] = True
            update_code()

    listener = liblo.ServerThread(listen_port)
    listener.add_method(None, None, osc_handle)
    listener.start()

    watcher = watch_file(file_name, update_code)
    try:
        logger.info("sending /ping messages to the server")
        while not state["server-responding"]:
            osc_send(server_addr, "/ping")
            sleep(1)
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        watcher.stop()
        listener.stop()
    watcher.join()

if __name__ == "__main__":
    main()
