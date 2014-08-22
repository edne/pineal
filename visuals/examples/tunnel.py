import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a


def loop():
    g.colorMode("hsv")

    h = a.note
    g.fill(h,1,1,a.amp*0.05)
    #noStroke()

    g.colorMode("rgb")
    g.stroke(a.high*5,a.amp*10)
    g.strokeWeight(2)

    g.colorMode("hsv")

    g.pushMatrix()
    #g.rotateX(pi/2)
    l = a.bass*100 + 2
    for i in xrange(50):
        g.fill(h,1,1,a.amp*0.01)
        g.square(l)
        l *= 0.9
        g.rotate(a.bass*0.2+m.pi/4)
        h += 0.01
    g.popMatrix()
