#!/usr/bin/env python3
# from time import time
import numpy as np
import pineal
from pineal.graphic import polygon, layer, window, stroke_weight
from pineal.listener import get_audio_data


pineal.run(__file__)


def rms(x):
    return np.sqrt(np.mean(np.square(x)))


def draw():
    stroke_weight(4)
    r, l = get_audio_data()

    with window('master'):
        # TODO: fill layer
        polygon(4, [0, 0.5], fill=True)\
            .scale(4)\
            .draw()

        polygon(4, [1], fill=False)\
            .draw()

        polygon(4, [1], fill=False)\
            .scale(rms(r) * 0.4)\
            .rotate(0*rms(l), [1, 0, 0])\
            .draw()

        layer('master')\
            .scale(0.1 + rms(r))\
            .draw()

        layer('master')\
            .scale(0.99 + rms(r))\
            .draw()

    with window('monitor', show_fps=True):
        layer('master').draw()
