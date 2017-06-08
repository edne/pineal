#!/usr/bin/env python3
from time import sleep
from threading import Thread
import logging

from pineal.renderer import render
from pineal.watcher import watch

logging.basicConfig(level=logging.DEBUG)  # TODO: take it from conf


def run_thread(f):
    t = Thread(target=f)
    t.daemon = True
    t.start()


if __name__ == '__main__':
    run_thread(render)
    run_thread(watch)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print()
