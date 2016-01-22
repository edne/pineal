#!/usr/bin/env python
from __future__ import print_function
from time import sleep
from sys import argv
from pineal.visions import load


def main(file_name):
    "Main function"

    vision = load(file_name)
    try:
        while True:
            vision.loop()
            sleep(1.0/120)
    except KeyboardInterrupt:
        vision.stop()

    vision.join()

if __name__ == "__main__":
    if argv[1:]:
        main(argv[1])
    else:
        print("Usage: ", argv[0], "filename")
