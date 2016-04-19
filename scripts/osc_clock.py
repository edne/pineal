#!/usr/bin/env python
from __future__ import print_function
from time import sleep
from osc import send

bpm = 80
addr = "7172"


def main():
    "Main function"
    try:
        send(addr, "/beat/enable", True)
        while True:
            sleep(60.0 / bpm)  # TODO: a real timer
            send(addr, "/beat", 1)
    except KeyboardInterrupt:
        send(addr, "/beat/enable", False)
        print("OSC Clock stopped")

if __name__ == "__main__":
    main()
