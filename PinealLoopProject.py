#!/usr/bin/python
from sys import argv
import threading
from subprocess import Popen
import pineal

if __name__=='__main__':

    MODULES = ['core', 'audio', 'gui']
    setted = [p for p in MODULES if '--'+p in argv]
    modules = setted or MODULES

    if modules[1:]:
        ths = [
            threading.Thread(   # threads for wait Popens
                target = Popen( # a Popen for each module
                    [__file__] + ['--'+m] +
                    [
                        arg     # same parameters
                        for arg in argv[1:]
                        if arg not in ('--'+M for M in MODULES)
                    ]
                ).communicate
            )
            for m in modules
        ]
        for t in ths:
            t.start()
        try:
            for t in ths:
                t.join()
        except KeyboardInterrupt:
            pass
    else:
        pineal.main()
