import math as m
from time import time
import livecoding.graphic as g
import livecoding.audio as a


def loop():
    rad = 1.0

    g.strokeWeight(2)

    g.colorMode("hsv")
    hue = time()/4 % 1.0
    g.stroke(hue + a.note*0.2, 0.2 + 0.01*a.amp)

    g.colorMode("rgb")
    g.fill(g.noise()*a.high*20)

    g.square(rad * (1+a.bass*8))
