import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a
import pineal.livecoding.osc as osc

n = 9


def occhio(x,y,r):
    g.pushMatrix()
    g.translate(x,y)

    g.stroke(0,0,0.5,1)
    g.fill(0,0,0.6, 0.1*a.amp)

    #g.pushMatrix()
    #g.translate(0,0, -0.3-a.amp*4)
    #g.rotate(0, m.pi*g.noise(),m.pi*g.noise())
    #g.circle(0,0, r*(m.exp(a.bass*16)-1))
    #g.square(r*(m.exp(a.bass*16)-1)*2)
    #g.cube(r*(m.exp(a.bass*16)-1)*2)
    #g.popMatrix()

    g.stroke(0,0,1,a.amp*0)
    g.fill(a.note,m.log(a.amp+1))

    g.pushMatrix()
    g.translate(0,0, a.high*g.noise())
    #g.rotate(0, m.pi*g.noise(),m.pi*g.noise())
    #g.circle(0,0, r*(m.exp(a.high/a.amp)-1))
    #g.square(r*(m.exp(a.bass*16)-2)*2)
    g.cube(r*(m.exp(a.bass*16)-1)*2)
    g.popMatrix()

    if a.high<a.amp*0.5:
        g.fill(0,0,0,1)
    else:
        g.fill(0,0,1,a.high*16)

    g.pushMatrix()
    g.translate(0,0, a.amp*8 + a.high*g.noise())
    g.rotate(0, m.pi*g.noise(),m.pi*g.noise())
    #g.circle(0,0, r*(m.exp(a.high*8)-1))
    #g.square(r*(m.exp(a.high*8)-1)*2)
    #g.cube(r*(m.exp(a.high*8)-1)*2)
    g.popMatrix()

    g.popMatrix()


def loop():
    g.colorMode('hsv')
    g.strokeWeight(1.4)

    occhio(0,0,1)

    n = 20
    for i in xrange(n):
        alpha = i*2*m.pi/n + g.noise()*a.high*8*a.bass*8
        r = (m.exp(a.bass*8)-1)*(1 + m.sin(i + 10*time()))
        g.pushMatrix()
        g.rotate(0, m.pi*g.noise(),m.pi*g.noise())
        occhio(r*m.cos(alpha),r*m.sin(alpha),(0.5 + a.bass) )
        g.popMatrix()
