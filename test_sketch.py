#!/usr/bin/env python3
from time import time
import numpy as np
import pineal
from pineal.core import polygon, layer, window, stroke_weight
from pineal.listener import get_audio_data


pineal.run(__file__)


def rms(x):
    return np.sqrt(np.mean(np.square(x)))


def draw():
    stroke_weight(2)
    r, l = get_audio_data()

    with window('master'):
        # TODO: fill layer
        polygon(4, [0, 0, 0, 0.1])\
            .scale(4)\
            .draw()

        polygon(4, [1, 1, 1], fill=False)\
            .draw()

        layer('master')\
            .scale(time() % 1)\
            .draw()

        polygon(4, [1, 1, 1])\
            .scale(rms(r) * 4)\
            .draw()

    with window('monitor', show_fps=True):
        layer('master').draw()
