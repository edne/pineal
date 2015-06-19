from lib.graphic import *
import lib.audio as audio
from math import *
from random import *

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")


def draw():
    strokeWeight(4)
    c = 8*amp() + 0.1

    do(
        turnaround(1),  # 23
        scale(0.9),
        frame,
    )()

    some = do(
        pwired(3)(rgb(0, 0, 1)),
    )

    n = 3 + int(8*bass())
    do(
        some,
        turnaround(n),
        scale(0.9 + high()),
        pwired(4)(rgb(1, 4*amp())),
        translate(1 - 4*bass()),
        scale(0.1),
        psolid(n)(rgb(1, 0*0.1)),
        pwired(n)(hsv(1 - c, 0*c)),
    )()
