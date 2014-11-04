from sys import argv, exit

def parse():
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
