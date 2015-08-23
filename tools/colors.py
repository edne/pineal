import pyglet.gl as gl


def stroke_weight(w):
    "OpenGL lines width"
    gl.glLineWidth(w)


def color(something, alpha=1):
    "try to cast everything to [r, g, b, a]"

    if len(something) == 4:
        return something

    elif len(something) == 3:
        return something + [alpha]

    else:
        raise TypeError("Invalid color")


def rgb(r, g, b):
    return [r, g, b]


def rgba(r, g, b, a):
    return [r, g, b, a]
