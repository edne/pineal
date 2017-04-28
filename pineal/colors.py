import pyglet.gl as gl
from math import floor, ceil


default_colors = {
    'red': (1, 0, 0),
    'green': (0, 1, 0),
    'blue': (0, 0, 1),

    'yellow': (1, 1, 0),
    'cyan': (0, 1, 1),
    'magenta': (1, 0, 1),

    'white': (1, 1, 1),
    'black': (0, 0, 0),
}


def stroke_weight(w):
    "OpenGL lines width"
    # TODO: make it an effect
    gl.glLineWidth(w)


def color(x, alpha=1):
    "try to cast everything to (r, g, b, a)"

    if len(x) == 4:
        return tuple(x)

    elif len(x) == 3:
        return tuple(x) + (alpha, )

    else:
        raise TypeError("Invalid color")


def from_palette(pal, index):
    if index > 1:
        index = index % 1
    index = index * (len(pal) - 1)

    i0 = int(floor(index))
    i1 = int(ceil(index))

    c0 = color(pal[i0])
    c1 = color(pal[i1])
    v = index - i0

    # TODO: test this
    out = tuple(v*c1[i] + (1-v)*c0[i]
                for i in range(4))

    return out
