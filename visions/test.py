from lib.graphic import *
import lib.audio as audio
from math import *
from random import *

amp = audio.source("AMP")


def draw():
    strokeWeight(4)

    @turnaround(23)
    @scale(0.9)
    def feedback():
        frame()

    @turnaround(2)
    @translate(0.5 + amp())
    @scale(0.4)
    def square():
        c = 8*amp()
        psolid(4)(rgb(1, c))
        pwired(4)(hsv(1 - c, c))

    feedback()
    square()
