from lib.graphic import *
import lib.audio as audio
from math import *
from random import *
from time import time


amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")


p = Polygon(4)
frame = Frame()


# @grid(4, 2)
# @turnaround(4)
@turnaround(3)
def a():
    scale((amp()*0.5 + bass()*2 + 0.5*gauss(0, 1*high())) + sin(time2rad()))
    rotate(time2rad(2))
    translate(0.1 + 20*bass())
    p.r = 0.04 + 1*high() + amp()*0.2 + 8*bass()
    # p.fill = hsv(time(), 0)
    p.fill = rgb(0, 0.5 + 0.0*bass())
    p.stroke = hsv(time())

    p.draw()


@turnaround(2)
def fb1():
    scale(0.99 + 0.5*amp())
    frame.draw()
    scale(bass()*0.5 + 0.5)
    frame.draw()


@turnaround(8)
@pushmatrix
def b():
    rotate(time2rad(0.4))
    # scale(1, bass())
    translate(2*amp() + 0.5)
    rotate(pi/4)
    p.r = 2*bass() + 0.001
    p.fill = rgb(0, bass())
    p.stroke = hsv(time())

    p.draw()


@turnaround(7)
@pushmatrix
def c():
    # scale(10*high() + 0.5*bass())
    translate(0.1 + 4*bass() + high())
    # scale(1, amp())
    rotate(pi/4)
    p.r = amp() + 0.001
    # p.fill = rgb(gauss(0.5, 5*high()), 1 * gauss(0.0, 10*high()))
    p.fill = rgb(0, 0)
    p.stroke = hsv(0.3 + time())
    p.draw()


def draw():
    strokeWeight(4)

    # a()
    b()
    c()
    fb1()
