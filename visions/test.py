from lib.graphic import *
import lib.audio as audio
from math import *
from random import *

amp = audio.source("AMP")
p = Polygon(4)
frame = Frame()
img = Image("alquemix")


@turnaround(2)
@pushmatrix
def a():
    translate(0.5)
    scale(0.4)

    c = 8*amp()
    p.fill = rgb(1, c)
    p.stroke = rgb(1 - c, c)

    p.draw()
    img.blit()


@turnaround(23)
def feedback():
    scale(0.9)
    frame.blit()


def draw():
    strokeWeight(4)

    feedback()
    a()
