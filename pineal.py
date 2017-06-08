#!/usr/bin/env python3
from time import sleep
import logging

from pineal.osc import receive
from pineal.renderer import render
from pineal.watcher import watch

import config

logging.basicConfig(level=(logging.DEBUG
                           if config.log_level == 'debug'
                           else logging.WARNING))


if __name__ == '__main__':
    osc_addr = config.osc_addr
    _, port = osc_addr
    file_name = config.file_name

    receive(port)
    render(file_name)
    watch(file_name, osc_addr)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print()
