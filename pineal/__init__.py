from sys import argv, exit
from core import Core
from audio import Audio
from web import Web
from gui import Gui

CLASSES = [Core, Audio, Web, Gui]


def parser():
    if [arg for arg in argv if arg in ('-h','--help')]:
        print '\nYou can remove modules with --no-module'
        print 'or add specific modules with --module'
        print 'Modules:'
        for Cl in CLASSES:
            print '  %s\t%s' % (Cl.__name__.lower(), Cl.__doc__)
        exit(0)

    params = [Cl.__name__.lower() for Cl in CLASSES]

    # exclude paramemeters with --no-classname
    excluded = [p for p in params if '--no-'+p in argv]
    if excluded:
        return [p for p in params if p not in excluded]
    # set parameters with --classname
    setted = [p for p in params if '--'+p in argv]
    # else run everything
    return setted or params


def main():

    params = parser()
    print params
    procs = [Cl() for Cl in CLASSES if Cl.__name__.lower() in params]

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
