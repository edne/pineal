from tools import *
from math import *
from random import *

from lib.audio import amp, bass, high


def draw():
    strokeWeight(5)

    Layer("out")()

    n = 4
    with Layer("asd"):
        Scale(0.9 + high())(
            Turnaround(7)(
                Layer("out")))()

        Turnaround(4)(
            Rotate(time2rad())(
                Translate(0.5 + 8*bass())(
                    Scale(0.1 + 4*bass())(
                        Psolid(n, rgb(0.0, 1.0)),
                        Pwired(n, hsv(2*time(), 1 - bass()))))))()

    with Layer("out"):
        Layer("asd")()
