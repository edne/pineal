from lib.graphic import *
import lib.audio as audio
from math import *
from random import *
from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")

p = Polygon(30)
frame = Frame()


@turnaround(6)
def a():
    translate(0.1 + amp())
    scale(0.04)
    p.fill = hsv(time())
    p.stroke = rgb(0, 0)

    p.draw()


def feedback():
    scale(0.98 + amp())
    frame.draw()
    scale(0.5 / (0.98 + amp()))
    frame.draw()


def draw():
    strokeWeight(4)

    feedback()
    rotate(time2rad(2))
    a()
