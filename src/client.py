#!/usr/bin/env python
from __future__ import print_function
import os
from sys import argv
import readline
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

        server_addr = os.environ.get("SERVER_ADDR", "127.0.0.1:7172")
        listen_port = os.environ.get("LISTEN_PORT", 7173)
        listen_port = int(listen_port)

        self.server_responding = False
        self.server = liblo.Address("osc.udp://{}/"
                                    .format(check_address(server_addr)))
        self.watchers = []
        self.listener = liblo.ServerThread(listen_port)
        self.listener.add_method(None, None, self.handle_osc)
        self.listener.start()  # TODO: start outside __init__

        self._running = False

        self.commands = {}

        readline.parse_and_bind("tab: complete")

    def add_command(self, name, function=None):
        "Add a new command to the command line interface"
        if function:
            self.commands[name] = function
        else:
            # used as decorator
            def decorator(f):
                self.commands[name] = f
                return f
            return decorator

    def handle_osc(self, path, msg):
        "Handle OSC events"
        if path == "/ack":
            logger.info("/ack received, sending code")
            self.server_responding = True
        if path == "/error":
            logger.info("/error received: {}".format(msg[0]))

    def handle_command(self, command, *args):
        "Handle user commands"
        if command in self.commands:
            self.commands[command](*args)

    def send(self, path, *msg):
        "Send message on a given path"
        logger.info("Sending to {0}".format(path))
        liblo.send(self.server, path, *msg)

    def main_loop(self):
        "Keep looping"

        try:  # future proof
            _input = raw_input
        except NameError:
            _input = input

        self._running = True
        try:
            while self._running:
                line = _input("> ").split()
                if line:
                    command = line[0]
                    args = line[1:]
                    self.handle_command(command, *args)
        except KeyboardInterrupt:
            logger.info("\rClosed with ^C")
            self.handle_command("exit")


client = Frontend()


@client.add_command("ping")
def ping():
    "Send /ping to the server untill /ack response"
    logger.info("sending /ping messages to the server")
    while not client.server_responding:
        client.send("/ping")
        sleep(1)


@client.add_command("run")
def run(file_name):
    "Read a file and send its content to /run-code"
    with open(file_name) as f:
        logger.info("Sending content of {}".format(file_name))
        client.send("/run-code", f.read())


@client.add_command("watch")
def watch(file_name):
    "Watch for changes in a file and send it to /run-code each time"
    w = watch_file(file_name,
                   lambda: client.run(file_name))
    client.watchers.append(w)

    run(file_name)


@client.add_command("exit")
def exit():
    "Ask the server to exit, stop listening and stop all the watchers"
    client._running = False
    client.send("/exit")
    client.listener.stop()
    logger.info("Closing watchers")
    for w in client.watchers:
        w.stop()
        w.join()


def main():
    "Main function"

    if argv[1:]:
        ping()
        client.handle_command(*argv[1:])

    client.main_loop()

if __name__ == "__main__":
    main()
