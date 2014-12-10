#!/usr/bin/python
from pineal.core import Core
from pineal.loader import Loader
from pineal.audio import Audio

if __name__=='__main__':
    ths = [
        Core(),
        Loader(),
        Audio()
    ]
    for t in ths:
        t.start()
    try:
        for t in ths:
            t.join(5)
    except KeyboardInterrupt:
        pass

    for t in ths:
        t.stop()
