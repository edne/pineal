#!/usr/bin/env python3
from sys import argv, exit
from time import sleep
import logging

from pineal.renderer import render
from pineal.watcher import watch
from pineal.listener import listen

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage:', argv[0], 'file.py')
        exit(1)

    file_name = argv[1]

    render(file_name)
    watch(file_name)
    listen('default', 2)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print()
