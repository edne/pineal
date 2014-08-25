import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a


def loop():
    g.colorMode("hsv")

    g.colorMode("rgb")
    g.stroke(1.0, 0.5)
    g.strokeWeight(2)

    g.colorMode("hsv")
    g.fill(0.5, 0.01)

    n = 9
    g.pushMatrix()
    g.rotate((time()/10)%(2 * m.pi))
    for i in xrange(n):
        g.rotate((2 * m.pi)/n)
        g.pushMatrix()

        for j in xrange(n):
            g.pushMatrix()
            r = (j+1)*1.0/n + 0.1*j
            g.fill(0.5 + 0.05*j, 0.005)
            g.stroke(0.5 + 0.1*j, 0.1)
            g.strokeWeight(r+0.5)
            g.translate(j * 1.0/n)
            g.rotate((0.1*j + time()/10)%(2 * m.pi))
            g.polygon(0,0, r, 4)
            g.popMatrix()

        g.popMatrix()
    g.popMatrix()
