#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import subprocess
import threading
import readline
import logging
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import liblo

readline.parse_and_bind("tab: complete")

logger = logging.getLogger("frontend.py")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

history_file = os.environ.get("HISTORY_FILE", ".pineal_history")
server_command = os.environ.get("PINEAL_SERVER", "pineal")

server_addr = os.environ.get("SERVER_ADDR", "127.0.0.1:7172")
listen_port = os.environ.get("LISTEN_PORT", 7173)
listen_port = int(listen_port)


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
    observer.daemon = True
    observer.start()

    return observer


def check_address(addr):
    "If only port is specified send to localhost"
    splitted = str(addr).split(":")
    if splitted[1:]:
        return addr
    else:
        return ":".join(["localhost", splitted[0]])


class State(dict):
    "State class, like a dict but with . notation"

    def __getattr__(self, name):
        "Get dict field as attribute"
        return self[name]

    def __setattr__(self, name, value):
        "Set dict field as attribute"
        self[name] = value


state = State()
state.running = False
state.server_responding = False
state.server_errors = False

commands = {}
watchers = []


def handle_osc(path, msg):
    "Handle OSC events"
    if path == "/ack":
        logger.info("/ack received, sending code")
        state.server_responding = True

    if path == "/status/error":
        logger.error("/error received: {}".format(msg[0]))
        state.server_errors = True

    if path == "/status/working":
        state.server_errors = False


def add_command(name, function=None):
    "Add a new command to the command line interface"
    if function:
        commands[name] = function
    else:
        def decorator(f):
            "When add_command is used as decorator"
            commands[name] = f
            return f
        return decorator


def handle_command(command, *args):
    "Handle user commands"
    if command in commands:
        commands[command](*args)


@add_command("send")
def send(path, *msg):
    "Send message on a given path"
    logger.info("Sending to {0}".format(path))
    addr = liblo.Address("osc.udp://{}/"
                         .format(check_address(server_addr)))
    liblo.send(addr, path, *msg)


@add_command("ping")
def ping():
    "Send /ping to the server untill /ack response"
    logger.info("sending /ping messages to the server")
    while not state.server_responding:
        send("/ping")
        sleep(1)


@add_command("start")
def start_server():
    try:
        subprocess.Popen([server_command])
    except OSError:
        logger.error("Server command '{}' not found".format(server_command))
    else:
        ping()


@add_command("run")
def run(file_name):
    "Read a file and send its content to /run-code"
    with open(file_name) as f:
        logger.info("Sending content of {}".format(file_name))
        send("/run-code", f.read())


@add_command("exit")
def exit():
    "Ask the server to exit, stop listening and stop all the watchers"
    state.running = False
    send("/exit")


def main_loop():
    "Keep looping"

    try:  # future proof
        _input = raw_input
    except NameError:
        _input = input

    state.running = True
    try:
        while state.running:
            line = _input("> ").split()
            if line:
                command = line[0]
                args = line[1:]
                handle_command(command, *args)
    except KeyboardInterrupt:
        logger.info("\rClosed with ^C")
        exit()


@add_command("watch")
def watch(file_name):
    "Watch for changes in a file and send it to /run-code each time"
    start_server()
    w = watch_file(file_name,
                   lambda: run(file_name))
    watchers.append(w)
    th = threading.Thread(target=lambda: run(file_name))
    th.daemon = True
    th.start()
    main_loop()


@add_command("test")
def test(*files):
    "Test given files"
    start_server()
    for file_name in files:
        run(file_name)
        sleep(1)
        if state.server_errors:
            logger.error("Errors in file {}".format(file_name))
            send("/exit")
            sys.exit(1)
    exit()


def main():
    "Main function"
    listener = liblo.ServerThread(listen_port)
    listener.add_method(None, None, handle_osc)
    listener.start()

    if sys.argv[1:]:
        handle_command(*sys.argv[1:])
    else:
        try:
            readline.read_history_file(history_file)
        except IOError:
            logger.info("History file {} not present".format(history_file))
        main_loop()
        readline.write_history_file(history_file)

    sys.exit(0)  # it works most of the times

    logger.info("Stopping watchers")
    for w in watchers:
        w.stop()

    logger.info("Stopping OSC listener")
    listener.stop()  # hangs and there is no way to stop it

    logger.info("Closing")


if __name__ == "__main__":
    main()
