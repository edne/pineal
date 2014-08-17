import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a


def _loop():
    g.colorMode('hsv')
    g.strokeWeight(2)

    g.pushMatrix()

    g.rotateZ((time())%(2*m.pi))

    g.fill(0.4 + a.note/3, 0.2)
    g.pushMatrix()
    for i in xrange(9):
        g.polygon(1,0, 0.6+a.bass, 6)
        g.rotateZ(2*m.pi/9)
    g.popMatrix()

    g.rotateZ((-2*time())%(2*m.pi))

    g.fill(0.2 + a.note/3, 0.01 + a.high)
    g.stroke(0,0,0,1 )
    g.pushMatrix()
    for i in xrange(9):
        g.polygon(0.4,0, 0.6+a.bass, 6)
        g.rotateZ(2*m.pi/9)
    g.popMatrix()

    g.popMatrix()

    """
    g.fill(0.6, 0.2)
    g.pushMatrix()
    n = 9
    for i in range(n):
        g.polygon(1,0, 1.2, 9)
        g.rotateZ(2*m.pi/n)
    g.popMatrix()

    g.fill(0.4, 0.1)
    g.stroke(0.7, 0.6)
    g.pushMatrix()
    n = 9
    for i in range(n):
        g.polygon(0.5,0, 0.6, 3)
    g.popMatrix()
    """
