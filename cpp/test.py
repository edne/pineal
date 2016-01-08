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

        p.attribute("fill", color(0.5, 0.5, 0.5))
        p.attribute("stroke", color(0, 1, 0))
        p.attribute("line", 0.05)

        p.attribute("rotate", pi/4)
        p.attribute("translate", 0.5, 0)
        p.attribute("scale", 0.2)

        q = polygon(8)

        g = pineal.Group()
        g.add(q)
        g.add(p)

        w.render(g)


if __name__ == "__main__":
    test_all()
