from core import Core
from web import Web
from browser import Browser


def main():
    procs = [
        Core(),
        Web(),
        Browser()
    ]

    for p in procs:
        p.start()

    try:
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        print
        for p in procs:
            p.stop()
            p.join()
