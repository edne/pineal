from pineal.osc import get_source
from .colors import from_palette, color
from .primitives import draw_layer


def osc_in(path):
    def f(mult=1, add=0):
        val = get_source(path)()
        return val*mult + add

    return f


def palette(colors):
    def f(index, in_alpha=None):
        pal = [color(c) for c in colors]
        [r, g, b, a] = from_palette(pal, index)
        return [r, g, b,
                a if in_alpha is None else in_alpha]

    return f


def draw(name):
    draw_layer(name)
