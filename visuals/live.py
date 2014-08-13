import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a
import pineal.livecoding.osc as osc

n = 9


def star():
    for i in range(n):
        g.pushMatrix()
        g.triangle(0,0, 0.6+a.amp,0, a.note, a.amp*2)
        g.popMatrix()
        g.rotateZ( 2*m.pi/n )


def pol():
    for i in range(n):
        g.pushMatrix()
        g.translate(1.0)
        g.polygon(0,0, 0.8+a.bass, n)
        g.popMatrix()
        g.rotateZ( 2*m.pi/n )


def loop():
    g.colorMode('hsv')
    g.strokeWeight(1.4)

    g.stroke(0,0,1,1)
    g.fill(0.2*a.note+0.5,0.01)

    for i in range(n):
        g.pushMatrix()
        g.translate(0.6)
        pol()
        g.popMatrix()
        g.rotateZ( 2*m.pi/n )

    g.stroke(a.note,1)
    g.fill(0,0,0,1)

    for i in range(n):
        g.pushMatrix()
        g.translate(0.8)
        g.rotateZ( time() % (2*m.pi))
        star()
        g.popMatrix()
        g.rotateZ( 2*m.pi/n )
