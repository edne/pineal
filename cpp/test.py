from __future__ import print_function
from math import pi
import pineal


def test_all():
    "Test hopefully everything"
    window = pineal.Window.memo
    polygon = pineal.Polygon
    color = pineal.Color


    w = window("asd")
    while w.is_open():
        p = polygon(4)

        p.dispatch("fill", color(0.5, 0.5, 0.5))
        p.dispatch("stroke", color(0, 1, 0))
        p.dispatch("line", 0.05)

        p.dispatch("rotate", pi/4)
        p.dispatch("translate", 0.5, 0)
        p.dispatch("scale", 0.2)

        w.render(p)


if __name__ == "__main__":
    test_all()
