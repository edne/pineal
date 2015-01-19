from lib.graphic import *
import lib.audio as audio
from math import *
from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")
p = Polygon(3)
frame = Frame()


def draw():
    frame.r = 1.6
    frame.x = sin(0.2*time() % 2*pi)*0 +0.3 + bass()*100

    push()
    rotate(0.5*time() % 2*pi)

    for i in xrange(6):
        rotate(pi/3)
        frame.draw()
    pop()

    p.r = bass()*100
    #p.fill = hsv(2*time(), 0.1)
    p.stroke = hsv(2*time())
    p.fill = [0]
    #p.stroke = [1]
    strokeWeight(2)
    #p.fill = [1, 0.8]
    #p.fill = [time() % 1]
    push()
    rotate(time() % 2*pi)
    p.draw()
    pop()
