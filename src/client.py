#!/usr/bin/env python
from __future__ import print_function
import os
import sys
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


class Client(object):
    def __init__(self, server_addr, listen_port):
        "Init frontend"
        logger.info("Starting frontend")
        self.server = liblo.Address("osc.udp://{}/"
                                    .format(check_address(server_addr)))
        self.running = False
        self.server_responding = False
        self.server_errors = False
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

        if path == "/status/error":
            logger.error("/error received: {}".format(msg[0]))
            self.server_errors = True

        if path == "/status/working":
            self.server_errors = False

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

        self.running = True
        try:
            while self.running:
                line = _input("> ").split()
                if line:
                    command = line[0]
                    args = line[1:]
                    self.handle_command(command, *args)
        except KeyboardInterrupt:
            logger.info("\rClosed with ^C")
            self.handle_command("exit")


server_addr = os.environ.get("SERVER_ADDR", "127.0.0.1:7172")
listen_port = os.environ.get("LISTEN_PORT", 7173)
listen_port = int(listen_port)

client = Client(server_addr, listen_port)

watchers = []

listener = liblo.ServerThread(listen_port)
listener.add_method(None, None, client.handle_osc)
listener.start()


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
    watchers.append(w)
    run(file_name)


@client.add_command("exit")
def exit():
    "Ask the server to exit, stop listening and stop all the watchers"
    client.running = False
    client.send("/exit")


@client.add_command("test")
def test(*files):
    "Test given files"
    for file_name in files:
        run(file_name)
        sleep(1)
        if client.server_errors:
            logger.error("Errors in file {}".format(file_name))
            client.send("/exit")
            sys.exit(1)
    client.send("/exit")


def main():
    "Main function"
    if sys.argv[1:]:
        ping()
        client.handle_command(*sys.argv[1:])
    else:
        client.main_loop()


if __name__ == "__main__":
    main()
