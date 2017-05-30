#!/usr/bin/env python3
from time import sleep
from threading import Thread
import logging

from pineal.eye import eye
from pineal.coder import coder

logging.basicConfig(level=logging.DEBUG)


def run_thread(f):
    t = Thread(target=f)
    t.daemon = True
    t.start()


if __name__ == '__main__':
    run_thread(eye)
    run_thread(coder)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print()
