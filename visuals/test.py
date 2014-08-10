import math as m
from time import time
import pineal.livecoding.graphic as g
import pineal.livecoding.audio as a
import pineal.livecoding.osc as osc

osc.alpha = 1.0
osc.rad = 1.0


def loop():
    g.strokeWeight(2)
    g.noFill()

    g.rotateY(m.sin(time()/100))
    #g.polygon(0,0, 0.4, 10)
    for i in range(1,int(10 + 30*a.amp)):
        g.colorMode("rgb")
        g.noFill()
        g.stroke(a.note*0.4 + g.noise()*a.high*4)
        r = (a.bass + 0*m.sin(time()))*40.0/i
        g.circle(0,0, r)
        g.rotateX(a.high)

    """
    g.colorMode("hsv")

    h = audio.note * 0.2
    #g.noStroke()

    g.colorMode("rgb")
    g.stroke(g.noise()*audio.bass*4)
    g.strokeWeight(2)

    g.colorMode("hsv")

    g.pushMatrix()
    l = 0.5 + audio.amp + audio.bass
    for i in xrange(10):
        g.rotate((time()/10)%(2 * math.pi))

        g.fill(h, 1, 1, 0.2 + 0.01*audio.amp + audio.high)
        r = l + audio.bass*math.sin(i + 10*time())
        g.tetrahedron(r * osc.rad)

        l *= 0.9
        g.strokeWeight(l+0.7)
        g.rotate(math.pi/4)
        h += 0.01
    g.popMatrix()
    """
