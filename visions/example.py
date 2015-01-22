from lib.graphic import *
import lib.audio as audio
from math import *
from random import *
from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")
p = Polygon(4)
frame = Frame()


def draw():
    strokeWeight(4)
    p.r = 0.9
    p.fill = hsv(0.1 * time() % 2*pi  +0.3, 0.9)
    p.stroke = hsv(0.1 * time() % 2*pi)

    push()
    rotate(-0.3*time() % 2*pi)
    p.draw()
    pop()

    frame.r = 0.5
    frame.x = 0.5

    push()
    n = 8
    rotate(0.2*time() % 2*pi)
    rotate(-pi/2)
    for i in xrange(n):
        frame.draw()
        rotate(2*pi/n)
    pop()
