import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a


def loop():
    g.colorMode("hsv")

    h = a.note+0.4
    g.fill(h,1,1,0.05)
    #noStroke()

    g.colorMode("rgb")
    g.stroke(0.8)
    g.strokeWeight(2)

    g.colorMode("hsv")

    g.pushMatrix()
    l = 2.0
    for i in xrange(50):
        g.rotate((time()/10)%(2*m.pi))

        g.fill(h,1,1,0.05)
        g.square(l)

        l *= 0.9
        g.strokeWeight(l+0.7)
        g.rotate(a.bass+m.pi/4)
        h += 0.01
    g.popMatrix()