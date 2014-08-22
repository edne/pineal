import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a


def loop():
    g.colorMode("hsv")

    h = a.note+0.3
    g.fill(h,1,1,1)
    #g.noStroke()

    g.colorMode("rgb")
    g.stroke(0)
    g.strokeWeight(2)

    g.colorMode("hsv")

    g.pushMatrix()
    l = 1.0
    g.rotate((time()/10)%(2*m.pi))

    g.fill(h,1,1,0.1)
    n = 10
    l = 1.0
    r = 0.5
    g.pushMatrix()

    for i in xrange(4):
        g.fill(h+0.1*i,1,1,0.1)
        for j in xrange(n):
            g.rotate(2*m.pi/n)
            g.rotate((time()/10)%(2*m.pi), (time()/5)%(2*m.pi))
            g.translate(r)
            g.square(l)
            g.translate(-r)
        r *= 0.6
        l *= 0.4

    g.popMatrix()

    l *= 0.9
    g.strokeWeight(l+0.7)
    g.rotate(a.bass+m.pi/4)
    h += 0.01
    g.popMatrix()
