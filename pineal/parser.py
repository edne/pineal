from sys import argv, exit

def parse():
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

    return locals()
