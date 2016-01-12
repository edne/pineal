from __future__ import print_function


def test_python():
    "Test Python APIs"
    from math import pi
    import pineal

    window = pineal.Window.memo
    polygon = pineal.Polygon
    color = pineal.Color
    signal = pineal.Signal


    w = window("asd")
    while w.is_open():
        p1 = polygon(4)
        p2 = polygon(8)
        p3 = polygon(3)

        g = pineal.Group()
        g.add(p1)
        g.add(p2)

        t = pineal.Transform()
        t.add(g)
        t.add(p3)

        t.attribute("rotate", signal(pi/6))

        g.attribute("line", signal(0.05))
        g.attribute("fill", color(0.5))
        g.attribute("stroke", color(0, 1, 0))

        p1.attribute("fill", color(0, 1, 1))
        p1.attribute("rotation", signal(pi/4))
        p1.attribute("position", signal(0.5, 0))
        p1.attribute("radius", signal(0.5))

        p2.attribute("radius", signal(0.2))
        p2.attribute("stroke", color(0, 0, 1))

        p3.attribute("radius", signal(0.1))
        p3.attribute("position", signal(0, 0.1))

        w.render(t)


def test_lisp():
    "Test DSL"
    import hy
    import test_lisp


if __name__ == "__main__":
    # test_python()
    test_lisp()
