#!/usr/bin/env python3
from time import sleep
import logging

from pineal.osc import receive
from pineal.renderer import render
from pineal.watcher import watch

logging.basicConfig(level=logging.DEBUG)  # TODO: take it from conf


if __name__ == '__main__':
    receive()
    render()
    watch()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print()
