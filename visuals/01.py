import math as m
from time import time
from pineal.livecoding import dt
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a


rad = 0.0
rad2 = 1.0
hue = 0.3


def cubo1():
    g.pushMatrix()

    g.colorMode('hsv')
    #g.stroke(hue + a.note*0.5, 0.08 + a.amp)
    g.stroke(hue + a.note*0.3, 1,1)

    g.colorMode("hsv")

    n = 10
    #g.scale(0.5)
    #g.rotate(0,0.1*time()%2*m.pi)
    for i in xrange(n):
        g.rotate(0.00*i * a.amp, 0.2*i + 2*m.pi/n, 0*2*m.pi/n)
        #g.scale(0.5 + a.bass*0.1 - a.amp*2)
        #g.translate(0, 4*a.bass - 0.04)
        #g.noStroke()
        g.fill(hue + a.note*0.3 + i*0.4/n, a.amp+0.1)
        #g.cube(0.8 * a.bass*8)
        g.pushMatrix()
        g.rotateX(i*0.05*time()%2*m.pi)
        #g.translate(0.0, 0.4)
        #g.rotate( 0.1 * time()%2*m.pi)
        #g.polygon(0,0, rad * (0.8 + 0.8 * a.bass*4 + a.high*2*g.noise()), 3)
        #g.tetrahedron(rad * (a.note*0.5 + 1.0 + 0.8 * a.bass*4 + a.high*2*g.noise()) )
        #g.cube(rad * (a.bass*6 - i*1.2/n) )
        #g.tetrahedron(rad * (a.bass*6 - i*1.0/n) )
        #g.polygon(0,0, rad * (a.bass*6 - i*1.0/n), 3)
        #g.cube(rad * (a.bass*6 - i*1.0/n) + a.amp*2)
        #g.tetrahedron(rad * (a.bass*6 - i*1.0/n) )
        g.polygon(0,0, rad * (a.bass*8 - i*1.2/n) + i*0.2/n + a.amp*g.noise(), 60 )
        g.popMatrix()

        #g.colorMode("rgb")
        #g.fill(0.8, 0.2)
        #g.square(a.amp*8 + a.high*g.noise())
        #g.cube(a.amp*8 + a.high*g.noise())

    g.popMatrix()


def cubo2():
    g.pushMatrix()

    g.colorMode('hsv')
    g.stroke(hue + a.note*0.3, 1,1)
    g.fill(hue + a.note*0.3, a.amp+0.1)

    n = 2
    for i in xrange(n):
        g.pushMatrix()
        g.polygon(0,0, rad2 *(0.2 + a.bass*8) * (i+1)*1.0/n, 60 )
        g.rotate(0, time()%2*m.pi + i*m.pi/n)
        g.popMatrix()

    g.popMatrix()


def ring(h0=0.0):
    g.colorMode('hsv')
    g.pushMatrix()
    #cubo1()
    #cubo2()
    n = 8
    for i in  xrange(n):
        g.fill(h0 +hue + a.note*0.3, (a.amp + a.bass)*0.005)

        g.rotate(i*2*m.pi/n)
        g.pushMatrix()
        g.translate(0.2+2*a.bass)
        g.rotate(-0.2*time()%2*m.pi)

        g.colorMode('hsv')
        g.stroke(hue + a.note*0.3 + h0, 1,1)

        g.polygon(0.5,0, rad + a.bass + a.high*5*g.noise(), 4)
        g.pushMatrix()
        g.translate(a.bass*4 + 40*a.high)
        g.rotate(0, 0.4*time()%2*m.pi)

        g.fill(h0 +hue + a.note*0.4, (a.amp + a.bass)*3)
        g.polygon(0.5,0, rad*(1 + a.bass + a.high*5*g.noise()), 30)
        #g.tetrahedron(rad + a.bass + a.high*5*g.noise())
        g.popMatrix()

        #g.colorMode('rgb')
        #g.stroke(hue + a.note*0.3 + h0, 1,0.1*a.bass)
        g.fill(h0 +hue + a.note*0.3, (a.amp + a.bass)*0.0005)

        #g.polygon(0,0, 0.4*rad + a.amp*4, 3)
        #g.cube(0.4*rad + a.amp*4)

        g.popMatrix()
    g.popMatrix()


def loop():
    g.strokeWeight(2)
    g.colorMode('rgb')

    g.pushMatrix()
    ring()
    g.scale(2.0)
    #ring(0.1)
    g.popMatrix()
