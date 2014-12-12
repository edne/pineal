#!/usr/bin/python
import hy
from core import Core
from coder import Coder
from ear import Ear

if __name__=='__main__':
    ths = [
        Core(),
        Ear(),
        Coder(),
    ]
    for t in ths:
        t.start()

    try:
        while True:
            for t in ths:
                t.join(1)
    except KeyboardInterrupt:
        pass

    for t in ths:
        t.stop()
