from sys import argv, exit

from core import Core
from audio import Audio
from gui import Gui

from pineal.help import help_string


def parse():
    if [arg for arg in argv if arg in ('-h','--help')]:
        print help_string()
        exit(0)

    for kw in ('render','output'):
        if '--'+kw+'-size' in argv:
            i = argv.index('--'+kw+'-size')
            if argv[i+1:]:
                splitted = argv[i+1].split('x')
                if len(splitted) == 2:
                    if kw == 'render':
                        RENDER_SIZE = (int(splitted[0]), int(splitted[1]))
                    if kw == 'output':
                        FULLSCREEN = False
                        OUTPUT_SIZE = (int(splitted[0]), int(splitted[1]))

    backends = ('portaudio', 'jack', 'coreaudio')
    setted = [b for b in backends if '--'+b in argv]
    if setted:
        BACKEND = setted[0]

    for k in ('osc-core','osc-gui'):
        if '--'+k in argv:
            i = argv.index('--'+k)
            if argv[i+1:]:
                splitted = argv[i+1].split(':')
                if len(splitted) == 2:
                    addrs[k] = (splitted[0], int(splitted[1]))

    CLASSES = [Core, Audio, Gui]
    MODULES = [Cl.__name__.lower() for Cl in CLASSES]

    setted = [p for p in MODULES if '--'+p in argv]
    MODULES = setted or MODULES

    return locals()
