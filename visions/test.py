from lib.graphic import *
import lib.audio as audio
from math import *
from random import *

amp = audio.source("AMP")


@turnaround(2)
@pushmatrix
def a():
    translate(0.5)
    scale(0.4)

    c = 8*amp()
    psolid(4)(rgb(1, c))
    pwired(4)(hsv(1 - c, c))


@turnaround(23)
def feedback():
    scale(0.9)
    frame()


def draw():
    strokeWeight(4)

    feedback()
    a()
