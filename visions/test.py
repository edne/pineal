from lib.graphic import *
import lib.audio as audio
from math import *
from random import *


amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")


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
            psolid(n)(rgb(0, 0.5)),
            pwired(n)(hsv(2*time(), 1 - bass())),
        )()

    with fb2:
        fb1()
