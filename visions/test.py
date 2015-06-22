from lib.graphic import *
import lib.audio as audio
from math import *
from random import *

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")


def draw():
    strokeWeight(5)

    do(
        turnaround(7),
        scale(0.92 + 8*bass() + 4*amp()),
        frame,
    )()

    do(
        scale(0.94 + 0*bass()),
        frame,
    )()

    n = 4
    do(
        turnaround(4 * int(100*bass()) or 4),
        translate(0.5 + 8*bass()),
        scale(4*bass()),
        scale(2 + 16*amp()),
        psolid(n)(rgb(0, 0.5)),
        pwired(n)(hsv(2*time(), 1 - bass())),
    )()
