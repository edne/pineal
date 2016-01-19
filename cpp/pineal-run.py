#!/usr/bin/env python
from __future__ import print_function
from sys import argv
import hy
from pineal.utils import hy_eval_string


def main(file_name):
    "Main function"
    ns = {}  # namespace

    with open(file_name) as f:
        hy_eval_string(f.read(), ns)

    try:
        while True:
            ns["loop"]()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    if argv[1:]:
        main(argv[1])
    else:
        print("Usage: ", argv[0], "filename")
