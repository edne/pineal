from __future__ import print_function
from math import pi
import pineal


def test_all():
    "Test hopefully everything"
    window = pineal.Window.memo
    polygon = pineal.Polygon
    color = pineal.Color
    while window("asd").is_open():
        p = polygon(4)
        p.fill(color(0.5, 0.5, 0.5))
        p.stroke(color(0, 1, 0))
        p.line(0.05)

        p.rotate(pi/4)
        p.position(0.5, 0)
        p.scale(0.2)

        w = window("asd")
        w.render(p)


if __name__ == "__main__":
    test_all()
