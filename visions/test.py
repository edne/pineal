from tools import *
from lib.graphic import *
from math import *
from random import *

from lib.audio import amp, bass, high


def draw():
    strokeWeight(5)

    # fb = Framebuffer(800, 800)
    fb1 = frame_buffer("asd")
    fb2 = frame_buffer("fb2")

    fb2()

    n = 4
    with fb1:
        do(
            scale(0.9 + high()),
            turnaround(7),
            fb2,
            )()

        do(
            turnaround(4),
            rotate(time2rad()),
            translate(0.5 + 8*bass()),
            scale(0.1 + 4*bass()),
            psolid(n, rgb(0.0, 1.0)),
            pwired(n, hsv(2*time(), 1 - bass())),
        )()

    with fb2:
        fb1()
