import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a

rad = 1.0
hue = 0.5


def loop():
    g.colorMode("hsv")

    g.colorMode("rgb")
    g.stroke(g.noise()*a.high*20)
    g.strokeWeight(2)

    g.colorMode("hsv")
    g.fill(hue + a.note * 0.2, 0.2 + 0.01*a.amp)

    g.pushMatrix()
    g.rotate(0.2, 0.5)
    g.rotateX((time()/10)%(2 * m.pi))
    g.cube(rad + a.bass*8)
    g.popMatrix()
