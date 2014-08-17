from sys import argv, exit

_HELP = '\nPineal Loop Project\n'
_HELP +=  '===================\n\n'


VISUALS_PATH = '../../visuals'

TITLE = 'Pineal Loop Project'
TITLE_OVERVIEW = 'pineal-overview'
TITLE_BROWSER  = 'pineal-browser'

## Graphic
FULLSCREEN = True
OUTPUT_SIZE = (640,480)

if '--output-size' in argv:
    i = argv.index('--output-size')
    if i+1 < len(argv):
        splitted = argv[i+1].split('x')
        if len(splitted) == 2:
            FULLSCREEN = False
            OUTPUT_SIZE = (int(splitted[0]), int(splitted[1]))

_HELP += 'Graphic settings\n'
_HELP += '----------------\n'
_HELP += 'With `--output-size WIDTHxHEIGHT` you can set the size of output \
window (visible only with a secondary monitor), default is fullscreen\n\n'
##

## Audio backend
backends = ('portaudio', 'jack', 'coreaudio')
BACKEND = backends[0]

setted = [b for b in backends if '--'+b in argv]
if setted:
    BACKEND = setted[0]

_HELP += 'Audio backend\n'
_HELP += '-------------\n'
_HELP += 'Select the audio backend with %s.  \nDefault is %s\n\n' % (
    ', '.join(['`--%s`' % b for b in backends]),
    backends[0]
)
##


## Network
addrs = {
    'osc-core': ('localhost', 1420),
    'osc-web':  ('localhost', 1421),
    'http':  ('localhost', 42080)
}
for k in addrs.keys():
    if '--'+k in argv:
        i = argv.index('--'+k)
        if i+1 < len(argv):
            splitted = argv[i+1].split(':')
            if len(splitted) == 2:
                addrs[k] = (splitted[0], int(splitted[1]))
OSC_CORE = addrs['osc-core']
OSC_WEB  = addrs['osc-web']
HTTP  = addrs['http']

_HELP += 'Network\n'
_HELP += '-------\n'
_HELP += 'Set the OSC address of core application or the webserver\n\
with `--osc-core` or `--osc-web` followed by `ip:port`.  \n\
With `--http` you set the address of webserver\n\n'
##


## Modules
from core import Core
from audio import Audio
from web import Web
#from gui import Gui
from browser import Browser

CLASSES = [Core, Audio, Web, Browser]
MODULES = [Cl.__name__.lower() for Cl in CLASSES]

# exclude paramemeters with --no-classname
excluded = [p for p in MODULES if '--no-'+p in argv]
if excluded:
    MODULES = [p for p in MODULES if p not in excluded]
else:
    # else set parameters with --classname
    setted = [p for p in MODULES if '--'+p in argv]
    # else run everything
    MODULES = setted or MODULES

_HELP += 'Modules\n'
_HELP += '-------\n'
_HELP += 'Remove modules with `--no-module` '
_HELP += 'or add specific modules with `--module`\n'
_HELP += '(e.g. `--no-audio`)\n'
_HELP += '\n    Modules:\n'
for Cl in CLASSES:
    _HELP += '      %s%s%s\n' % (
        Cl.__name__.lower(),
        ' '*(12 - len(Cl.__name__)),
        Cl.__doc__
    )
##


## Help
if [arg for arg in argv if arg in ('-h','--help')]:
    print _HELP
    exit(0)
##
