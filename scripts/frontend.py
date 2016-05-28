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


class Frontend(object):
    def __init__(self, server_addr, listen_port):
        "Init frontend"
        logger.info("Starting frontend")
        # TODO: repl.command("command-name", method)
        self.server_responding = False
        self.server = liblo.Address("osc.udp://{}/"
                                    .format(check_address(server_addr)))
        self.watchers = []
        self.listener = liblo.ServerThread(listen_port)
        self.listener.add_method(None, None, self.handle_osc)
        self.listener.start()

    def handle_osc(self, path, msg):
        "Handle OSC events"
        if path == "/ack":
            logger.info("/ack received, sending code")
            self.server_responding = True

    def send(self, path, *msg):
        "Send message on a given path"
        logger.info("Sending to {0}".format(path))
        liblo.send(self.server, path, *msg)

    def wait_server(self):
        "Send /ping to the server untill /ack response"
        logger.info("sending /ping messages to the server")
        while not self.server_responding:
            self.send("/ping")
            sleep(1)

    def run_file(self, file_name):
        "Read a file and send its content to /run-code"
        with open(file_name) as f:
            logger.info("Sending content of {}".format(file_name))
            self.send("/run-code", f.read())

    def watch(self, file_name):
        "Watch for changes in a file and send it to /run-code each time"
        w = watch_file(file_name,
                       lambda: self.run_file(file_name))
        self.watchers.append(w)

    def exit(self):
        "Ask the server to exit, stop listening and stop all the watchers"
        self.send("/exit")
        self.listener.stop()
        for w in self.watchers:
            w.stop()
            w.join()


def main():
    "Main function"
    if len(argv) < 2:
        print("Watch a file for changes and send to pineal server")
        print("Usage:", argv[0], "file_to_watch [server_addr] [listen_port]")
        return

    server_addr = argv[2] if argv[2:] else "127.0.0.1:7172"
    listen_port = argv[3] if argv[3:] else 7173
    listen_port = int(listen_port)
    file_name = argv[1]

    frontend = Frontend(server_addr, listen_port)
    frontend.watch(file_name)
    try:
        frontend.wait_server()
        frontend.run_file(file_name)
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        logger.info("Closed with ^C")
    frontend.exit()

if __name__ == "__main__":
    main()
