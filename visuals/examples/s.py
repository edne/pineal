import math as m
from time import time
from pineal.livecoding import dt
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a

rad = 1.0


def loop():
    g.resetMatrix()
    g.strokeWeight(2)

    g.colorMode("hsv")

    #g.colorMode("rgb")

    b1 = 0
    n = 20
    for i in xrange(n):
        g.stroke(a.note*0.1*i + 0.2, 0.2 + 0.01*a.amp)
        g.fill(a.note*0.1*i + 0.3, 0.05*a.amp)
        g.pushMatrix()
        g.square(rad * (a.bass*8), a.bass*8*i)
        g.square(rad * (a.amp*4), 0, a.amp*4*i)
        g.square(rad * (a.high*8), a.high*8, b1*a.high*8)
        g.popMatrix()
        g.scale(0.4 + a.bass*1)
        g.rotate(m.pi/2 - 0*((0.2*time()%2*m.pi) + a.note*m.pi/n))
