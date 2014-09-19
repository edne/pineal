import math as m
from time import time
from pineal.livecoding import dt
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a

rad = 1.0
hue = 0.0
knob1 = 0.5
knob2 = 0.5
knob3 = 0.5


def uno():
    g.colorMode('rgb')
    g.fill(1.0, a.amp*0.4/(0.4+rad*10))
    g.stroke(1.0,0.4/(0.4+rad*5))

    g.pushMatrix()
    g.rotate(0,0,0.8)
    #g.polygon(0,0.1, rad*a.bass*4, 4)

    n = 8
    for i in xrange(n):
        rot = time()/4%2*m.pi
        g.pushMatrix()
        g.rotate(i*2*m.pi/n + rot)
        g.translate(0.5 + a.bass*8 + 2*a.high*g.noise())
        g.rotate(-rot)
        g.polygon(0,0, rad*0.8 - rad*0.04*i, 3)
        g.popMatrix()

    g.popMatrix()


def due():
    g.colorMode('rgb')
    g.fill(1.0, a.amp*0.1/(0.4+rad*10))
    g.stroke(1.0,0.8/(0.9+rad*10))

    g.pushMatrix()

    n = 20
    for i in xrange(n):

        g.pushMatrix()
        g.rotate(0, i*2*m.pi/n + time()*0.1 % 2*m.pi)
        g.rotate(0,0,i*2*m.pi/n + time()*0.06 % 2*m.pi)
        #g.polygon(0,0, a.bass*4*i*5*rad/n, 4)
        #g.circle(0,0, 100*i*rad/n)
        uno()
        g.popMatrix()

    g.popMatrix()


def tre():
    g.colorMode("hsv")
    n1 = int(knob1*10)+2
    n2 = int(knob2*10)+2
    g.pushMatrix()
    g.rotate(time()/10 % 2*m.pi)
    for i in xrange(n1):
        g.rotate(2*m.pi/n1)
        g.pushMatrix()

        for j in xrange(n2):
            g.fill(hue+0.1*a.note + 0.003*j, 0.5/(n1*n2))
            g.stroke(hue+0.1*a.note + 0.005*j, 0.1)

            r = ((j+1)*1.0/n2 + 0.1*j)
            g.strokeWeight(r+0.5)

            g.pushMatrix()
            g.translate(j * 1.0/n2 + a.bass*2)
            g.rotate(0.1*j + time()/10 % 2*m.pi)
            g.polygon(0,0, r+a.high*4, 4)
            g.popMatrix()

        g.popMatrix()
    g.popMatrix()


def loop():
    g.strokeWeight(2)

    #uno()
    #due()
    #tre()
