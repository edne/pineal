import pyglet.gl as gl


def stroke_weight(w):
    "OpenGL lines width"
    gl.glLineWidth(w)


default_colors = {
    "r": [1, 0, 0],
    "g": [0, 1, 0],
    "b": [0, 0, 1],

    "y": [1, 1, 0],
    "c": [0, 1, 1],
    "m": [1, 0, 1],

    "w": [1, 1, 1],
    "k": [0, 0, 0],
}


def color(x, alpha=1):
    "try to cast everything to [r, g, b, a]"

    if x in default_colors.keys():
        return default_colors[x] + [alpha]

    elif len(x) == 4:
        return x

    elif len(x) == 3:
        return x + [alpha]

    else:
        raise TypeError("Invalid color")


def rgb(r, g, b):
    return [r, g, b]


def rgba(r, g, b, a):
    return [r, g, b, a]


def from_palette(pal, index):
    "A palette is a list of [r, g, b, a] lists"
    if index > 1:
        index = index % 1
    index = index * (len(pal) - 1)

    from math import floor, ceil
    i0 = int(floor(index))
    i1 = int(ceil(index))

    c0 = pal[i0]
    c1 = pal[i1]
    v = index - i0

    out = [0]*4
    for i in range(4):
        out[i] = v*c0[i] + (1-v)*c1[i]

    return out
