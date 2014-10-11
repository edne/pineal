from sys import argv, exit

VISUALS_PATH = '../../visuals'

TITLE = 'Pineal Loop Project'
TITLE_OVERVIEW = 'pineal-overview'
TITLE_BROWSER  = 'pineal-browser'

## Graphic
FULLSCREEN = True
RENDER_SIZE = (640,480)
OUTPUT_SIZE = (640,480)
##

BACKEND = 'portaudio'

OSC_CORE = ('localhost', 1420)
OSC_GUI  = ('localhost', 1421)

from pineal.parser import parse
globals().update(parse())
