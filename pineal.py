#!/usr/bin/env python3
from sys import argv, exit
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

    watch(file_name)
    listen('default', 2)

    try:
        render(file_name)  # blocking
    except KeyboardInterrupt:
        print()
