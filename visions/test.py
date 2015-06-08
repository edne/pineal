from lib.graphic import *
import lib.audio as audio
from math import *
from random import *

amp = audio.source("AMP")


def draw():
    strokeWeight(4)
    c = 8*amp() + 0.1

    do(
        turnaround(23),
        scale(0.9),
        frame,
    )

    do(
        turnaround(2),
        translate(0.5 + amp()),
        scale(0.4),
        psolid(4)(rgb(1, c)),
        pwired(4)(hsv(1 - c, c)),
    )

    do(
        scale(1 + amp()),
        pwired(4)(rgb(0, 1, 0)),
    )
