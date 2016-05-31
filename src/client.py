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
    def __init__(self):
        "Init frontend"
        logger.info("Starting frontend")
        # TODO: repl.command("command-name", method)

        server_addr = os.environ.get("SERVER_ADDR", "127.0.0.1:7172")
        listen_port = os.environ.get("LISTEN_PORT", 7173)
        listen_port = int(listen_port)

        self.server_responding = False
        self.server = liblo.Address("osc.udp://{}/"
                                    .format(check_address(server_addr)))
        self.watchers = []
        self.listener = liblo.ServerThread(listen_port)
        self.listener.add_method(None, None, self.handle_osc)
        self.listener.start()

        self._running = True

    def handle_osc(self, path, msg):
        "Handle OSC events"
        if path == "/ack":
            logger.info("/ack received, sending code")
            self.server_responding = True
        if path == "/error":
            logger.info("/error received: {}".format(msg[0]))

    def handle_command(self, command, *args):
        "Handle user commands"
        if command == "exit":
            self.exit()

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

    def run(self, file_name):
        "Read a file and send its content to /run-code"
        with open(file_name) as f:
            logger.info("Sending content of {}".format(file_name))
            self.send("/run-code", f.read())

    def watch(self, file_name):
        "Watch for changes in a file and send it to /run-code each time"
        w = watch_file(file_name,
                       lambda: self.run(file_name))
        self.watchers.append(w)
        self.run(file_name)

    def main_loop(self):
        "Keep looping"

        try:  # future proof
            _input = raw_input
        except NameError:
            _input = input

        try:
            while self._running:
                command = _input("> ")  # TODO: use libreadline
                self.handle_command(command)
        except KeyboardInterrupt:
            logger.info("\rClosed with ^C")
            self.exit()

    def exit(self):
        "Ask the server to exit, stop listening and stop all the watchers"
        self._running = False
        self.send("/exit")
        self.listener.stop()
        logger.info("Closing watchers")
        for w in self.watchers:
            w.stop()
            w.join()


def print_help():
    "Print the help"
    print("Watch a file for changes and send to pineal server")
    print("Usage:")
    print("      ", argv[0], "run file_to_run")
    print("      ", argv[0], "watch file_to_watch")


def get_argument(n):
    "Get the nth argument, dislay help and close if not present"
    arguments = argv[1:]
    if len(arguments) < n+1:
        print_help()
        os.exit(1)
    else:
        return arguments[n]


def main():
    "Main function"
    frontend = Frontend()
    frontend.wait_server()

    command = get_argument(0)

    if command == "run":
        file_name = get_argument(1)
        frontend.run(file_name)

    if command == "watch":
        file_name = get_argument(1)
        frontend.watch(file_name)

    frontend.main_loop()

if __name__ == "__main__":
    main()
