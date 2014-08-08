from core import Core
from audio import Audio
from web import Web
from gui import Gui


def main():
    procs = [
        Core(),
        Audio(),
        Web(),
        Gui(),
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
