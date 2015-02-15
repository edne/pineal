from lib.graphic import *
import lib.audio as audio
from math import *
from random import *
from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")

frame = Frame()

p = Polygon(4)
q = Polygon(20)


@turnaroud(5)
@pushmatrix
def realmagic():
    rotate((0.1*time()) % 2*pi)
    scale(0.8)
    frame.draw()


@turnaroud(7)
@pushmatrix
def atom(r, minr= 0.2):
    p.fill = rgb(sin(8*time()%2*pi)*0.2 + gauss(0, 0.2), 1)

    #p.fill = hsv( (1.2*time()) % 2*pi)
    #p.stroke = rgb(0)

    #p.stroke = hsv( 0.4 + 0.2*sin((2.2*time()) % 2*pi))
    #p.fill = rgb(0)

    #p.stroke = hsv( (1.9*time()) % 2*pi)
    #p.fill = hsv( (1.2*time()) % 2*pi, bass() + bass()*sin(2*time() % 2*pi) + 2*high())
    #p.fill = hsv(0.5,0)

    p.stroke = hsv(4*bass())

    #p.fill = hsv(gauss(0, 2*high()), 0.99)
    #p.fill = rgb(gauss(0, 2*high()), 0.99)

    #translate(-bass() + 0.8 + gauss(0, 0.1*bass()))
    translate(bass())
    scale(r * (2*bass() + amp() + minr))

    #rotate((time()) % 2*pi)
    p.draw()


def _atom():
    p.stroke = rgb(1)
    p.fill = rgb(0)

    scale(bass()*2 + 0.1)
    p.draw()

    translate(-bass()*4 + 0.8 + gauss(0, 0.0*bass()))

    #rotate((time()) % 2*pi)


@turnaroud(4)
@pushmatrix
def qu():
    q.fill = hsv(0.6, 8*high())
    q.stroke = hsv(0.6)
    translate(8*bass())
    scale(0.1)
    q.draw()


def draw():
    strokeWeight(4)
    atom(1)
    atom(2, 0.3)
    rotate(pi/2)
    #atom(-0.5)
    #rotate(0.05*time() % 2*pi)
    rotate(pi/4)

    realmagic()
    qu()
