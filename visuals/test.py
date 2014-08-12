import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a
import pineal.livecoding.osc as osc

osc.alpha = 1.0
osc.rad = 1.0


def _loop():
    g.colorMode("hsv")

    h = a.note * 0.2

    g.colorMode("rgb")
    g.stroke(g.noise()*a.bass*4)
    g.strokeWeight(2)

    g.colorMode("hsv")

    g.pushMatrix()
    l = 0.5 + a.amp + a.bass
    for i in xrange(10):
        g.rotate((time()/10)%(2 * m.pi))

        g.fill(h, 1, 1, 0.2 + 0.01*a.amp + a.high)
        r = l + a.bass*m.sin(i + 10*time())
        g.tetrahedron(r * osc.rad)

        l *= 0.9
        g.strokeWeight(l+0.7)
        g.rotate(m.pi/4)
        h += 0.01
    g.popMatrix()
