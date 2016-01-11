from __future__ import print_function


def test_python():
    "Test Python APIs"
    from math import pi
    import pineal

    "Test hopefully everything"
    window = pineal.Window.memo
    polygon = pineal.Polygon
    color = pineal.Color
    signal = pineal.Signal


    w = window("asd")
    while w.is_open():
        g = pineal.Group()

        # g.attribute("line", signal(0.05))
        # g.attribute("fill", color(0.5))
        # g.attribute("stroke", color(0, 1, 0))

        p = polygon(4)
        p.attribute("fill", color(0.0, 0.5, 0.5))
        p.attribute("rotate", signal(pi/4))
        p.attribute("translate", signal(0.5, 0))
        p.attribute("scale", signal(0.2))
        g.add(p)

        q = polygon(8)
        q.attribute("scale", signal(0.5))
        q.attribute("stroke", color(0, 1, 1))
        g.add(q)

        w.render(g)


def test_lisp():
    "Test DSL"
    import hy
    import test_lisp


if __name__ == "__main__":
    # test_python()
    test_lisp()
