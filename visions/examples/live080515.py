from lib.graphic import *
import lib.audio as audio
from math import *
from random import *
# from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")

frame = Frame()
square = Polygon(4)
img = Image("alquemix")

p = Polygon(3)


def high_noise():
    return max([gauss(0, 4*high())])


@pushmatrix
@turnaround(9)
def a():
    # rotate(time2rad(-2.5))

    translate(bass() + 8 * amp() + high_noise())
    scale(8*bass())  # cross

    # scale(4*amp() + 2*bass())  # heavy

    # p.fill = rgb(0, 0.5)
    # p.fill = hsv(time2rad(0.1), 0.5-amp())
    p.fill = hsv(time2rad(0.1), high_noise())
    p.stroke = hsv(0.2*high_noise() + time2rad(0.2))

    p.fill = rgb(0, 0.5)
    p.stroke = rgb(1, 1)

    p.draw()


@turnaround(8)
def b():
    translate(bass() + 2*amp() + 0.1*high_noise())
    rotate(time2rad(-2.5))
    scale(amp())

    p.fill = hsv(0.2 + time2rad(0.1), high_noise())
    p.stroke = hsv(0.2 + time2rad(0.2))

    # p.fill = rgb(0)

    p.draw()

    scale(0.2)
    translate(-0.5)
    a()


@pushmatrix
def feedback():
    rotate(high())
    scale(1.1)
    frame.draw()

    scale(0.9)
    frame.draw()

    scale(0.5)
    frame.draw()


def fd1():
    scale(0.5)
    feedback()
    scale(1.5)
    feedback()


@turnaround(4)
def fd2():
    translate(2*amp())
    scale(2*amp())
    feedback()


def draw():
    strokeWeight(4)

    # rotate(time2rad(0.2))

    feedback()
    # fd2()
    a()
    # b()

    # fd1()

    # scale(4*bass())
    # frame.draw()
