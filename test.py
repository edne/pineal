from pineal.core import polygon, layer, window
from time import time

with window('master'):
    polygon(4, [0, 0, 0, 0.1]).scale(4).draw()  # TODO: fill layer

    polygon(4, [1, 1, 1], fill=False).draw()
    layer('master').scale(time() % 1).draw()


with window('monitor', show_fps=True):
    layer('master').draw()
