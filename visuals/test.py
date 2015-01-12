from lib.graphic import Polygon, push, pop, rotate
import lib.audio as audio
from math import pi
from time import time

amp = audio.source("AMP")
p = Polygon(3)


def draw():
    #p.r = sin(time()) + 1
    #p.x = 0.7
    push()
    p.c = [1,1,1, 0.5]
    rotate(time() % 2*pi)
    p.draw()
    pop()
