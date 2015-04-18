from lib.graphic import *
import lib.audio as audio
from math import *
from random import *
# from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")
p = Polygon(4)
q = Polygon(4)
frame = Frame()


@turnaroud(3, 0.5)
@pushmatrix
def a():
    p.r = 0.4 + bass()
    # translate(bass()*4)

    p.fill = rgb(0, 0.5)
    p.stroke = rgb(1, 1)

    p.draw()


@pushmatrix
def b():
    q.fill = rgb(0, 0.08)
    q.stroke = rgb(2*time(), 1)
    scale(1+4*amp())
    q.draw()


@turnaroud(9)
def feedback():
    frame.r = 1.3
    frame.draw()

    frame.r = 0.5
    frame.draw()


def draw():
    strokeWeight(4)

    feedback()
    # rotate(time2rad())
    a()
    rotate(time2rad(-2))
    # b()
