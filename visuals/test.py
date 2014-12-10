import math as m
from time import time
from pineal.livecoding import dt
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a

rad = 1.0
hue = [0.0]


def loop():
    g.strokeWeight(2)

    hue[0] = hue[0] + dt
    g.colorMode("hsv")
    g.stroke(hue[0] + a.note*0.2, 0.2 + 0.01*a.amp)

    g.colorMode("rgb")
    g.fill(g.noise()*a.high*20)

    g.pushMatrix()
    g.rotate(0.2, 0.5)
    g.rotateX((time()/10)%(2 * m.pi))
    g.cube(rad * (1+a.bass*8))
    g.popMatrix()
