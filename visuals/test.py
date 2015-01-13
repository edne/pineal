from lib.graphic import *
import lib.audio as audio
from math import *
from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")
p = Polygon(4)


def draw():
    p.r = 1
    #p.c = [0, 0.5, 1, 0.8]
    p.c = hsv(0.4, 0.5)
    n = 1
    for i in range(n):
        push()
        #p.x = bass() * 4
        rotate(i*0.01*time() % 2*pi)
        p.draw()
        pop()
