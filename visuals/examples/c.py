import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a

rad = 1.0
hue = 0.5


def shape():
    g.pushMatrix()
    #g.rotateZ((-time()/5)%(2 * m.pi))
    g.square(rad * (0.02 + a.bass*0.1))
    g.popMatrix()


class Qualcosa(object):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def draw(self):
        g.square(0.1, self.x, self.y, self.z)


def loop():
    g.colorMode("hsv")

    g.colorMode("hsv")
    g.stroke(hue + a.note/2, 1.0)
    g.fill(0,0,1, 0.1)
    g.strokeWeight(2)

    #shape()

    n = 30
    r = 0.5
    g.pushMatrix()
    for i in xrange(n):
        g.pushMatrix()
        g.rotateZ( i*2*m.pi/n*2 + 0*(time()/10)%(2*m.pi) + m.sin(time()%(2*m.pi)+i*2*m.pi/n))
        g.translate(r*m.cos(i*2*m.pi/n),0, r*m.sin(i*2*m.pi/n))
        shape()
        g.popMatrix()
    g.popMatrix()
