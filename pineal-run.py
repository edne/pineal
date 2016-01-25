#!/usr/bin/env python
from __future__ import print_function
from time import sleep, time
from sys import argv
from pineal.visions import load


def main(file_name):
    "Main function"

    vision = load(file_name)
    t0 = time()
    try:
        while True:
            vision.loop()

            t1 = time()
            dt = t1-t0
            t0 = t1
            print("fps:", 1.0/dt, end="\r")

            sleep_time = 1.0/120 - dt
            if sleep_time > 0:
                sleep(sleep_time)
    except KeyboardInterrupt:
        vision.stop()

    vision.join()

if __name__ == "__main__":
    if argv[1:]:
        main(argv[1])
    else:
        print("Usage: ", argv[0], "filename")
