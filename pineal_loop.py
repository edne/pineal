#!/usr/bin/python
import hy
from pineal.core import Core
from coder import Coder
from ear import Ear
from watcher import Watcher

if __name__=='__main__':
    ths = [
        Core(),
        Ear(),
        Coder(),
        Watcher()
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
