import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a


def loop():
    g.colorMode("hsv")

    h = a.note
    g.fill(h,1,1,0.05)
    #g.noStroke()

    g.colorMode("rgb")
    g.stroke(0.8)
    g.strokeWeight(2)

    g.colorMode("hsv")

    g.pushMatrix()
    l = 1.0
    for i in xrange(10):
        #rotate((time/10)%(2*pi))

        g.fill(h,1,1,0.05)
        g.tetrahedron(l+m.sin(time()+i)*(1-a.bass*8))

        l *= 0.9
        g.strokeWeight(l+0.7)
        g.rotate(a.bass+m.pi/4)
        h += 0.01
    g.popMatrix()
