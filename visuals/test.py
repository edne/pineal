from lib.graphic import *
import lib.audio as audio
from math import *
from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")
p = Polygon(3)
frame = Frame()


def draw():
    frame.x = sin(0.2*time() % 2*pi)

    push()
    rotate(0.5*time() % 2*pi)
    for i in xrange(6):
        rotate(pi/3)
        frame.draw()
    pop()

    p.c = hsv(2*time(), 1)
    #p.c = [time() % 1]
    push()
    rotate(time() % 2*pi)
    p.draw()
    pop()
