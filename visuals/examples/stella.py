import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a

alpha = 1.0


def loop():
    g.pushMatrix()
    g.rotate((time())%(2 * m.pi))
    g.colorMode("hsv")

    h = a.note
    g.fill(h,1,1,a.amp*4 * alpha + 0.1)
    g.noStroke()

    g.pushMatrix()
    g.rotateX(m.pi/2)
    l = a.bass*10 + 2
    for i in xrange(100):
        g.square(l)
        l *= 0.9
        g.rotateY(a.bass+m.pi/4)
        g.rotateX(a.bass+m.pi/4)
    g.popMatrix()

    g.popMatrix()
