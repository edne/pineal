from lib.graphic import Polygon
import lib.audio as audio
from math import sin
from time import time

amp = audio.source("AMP")
p = Polygon(4)


def draw():
    p.r = sin(time()) + 1
    p.x = 0.7
    p.fill = [1,1,1, 0.5]
    p.draw()
