from core import Core
from audio import Audio
from web import Web
from browser import Browser


def main():
    procs = [
        Core(),
        Audio(),
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
        procs.reverse()
        for p in procs:
            p.stop()
            p.join()
