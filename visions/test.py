from tools import *
from lib.audio import amp, bass, high


def draw():
    strokeWeight(5)

    Layer("out")()

    n = 4
    Layer("layer1")(
        Scale(0.9 + high())(
            Turnaround(3)(
                Layer("out"))),

        Turnaround(4)(
            Rotate(time2rad())(
                Translate(0.5 + 8*amp())(
                    Pwired(n, hsv(2*time(), 1 - bass())),
                    Scale(0.1 + 4*bass())(
                        Psolid(n, rgb(0.0, 1)))))))()

    Layer("out")(
        Scale(1.0 - bass())(
            Layer("layer1")))()
