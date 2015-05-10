from lib.graphic import *
import lib.audio as audio
from math import *
from random import *
#from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")
p = Polygon(4)
q = Polygon(20)
frame = Frame()


@turnaround(2, 0.5)
@pushmatrix
def a():
    p.r = 0.4
    translate(bass()*4)

    p.fill = rgb(1, 0.5)
    p.stroke = rgb(0, 1)

    p.draw()


@turnaround(2)
@pushmatrix
def b():
    q.fill = hsv(0.6, 1)
    q.stroke = rgb(0)
    translate(4*amp())
    scale(0.1)
    q.draw()


@turnaround(13)
def feedback():
    frame.r = 0.5
    frame.x = 0.5

    frame.draw()


def draw():
    strokeWeight(4)

    rotate(time2rad())
    a()
    rotate(time2rad(-2))
    b()

    feedback()
