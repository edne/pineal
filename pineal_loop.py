#!/usr/bin/python
import hy
from pineal.core import Core
from pineal.loader import Loader
from coder import Coder
from ear import Ear

if __name__=='__main__':
    ths = [
        Ear(),
        Coder(),
        Core(),
        Loader(),
    ]
    for t in ths:
        t.start()

    try:
        while True:
            for t in ths:
                t.join(5)
    except KeyboardInterrupt:
        pass

    for t in ths:
        t.stop()
