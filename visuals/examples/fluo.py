import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a

rad = 1.0


def loop():
    g.strokeWeight(2)

    #g.rotateX(dt*2*(0.2+a.amp))
    #g.rotateY(dt*4*(0.2+a.amp))

    g.colorMode("hsv")
    g.fill(a.note*0.3, 0.004)

    g.colorMode("rgb")
    g.stroke(a.high*16, 1)

    r = (a.bass*4)*rad*10
    for i in xrange(100):
        r -= 16*a.high*rad
        g.cube(r)
