from __future__ import print_function
import pineal


def test_memo():
    "Test memoizing"
    window = pineal.Window.memo

    while window("asd").is_open():
        window("asd").display()


def test_child():
    "Test  child drawing"
    window = pineal.Window.memo
    polygon = pineal.Polygon

    while window("asd").is_open():
        window("asd").render(polygon(4))


def test_color():
    "Test coloring"
    window = pineal.Window.memo
    polygon = pineal.Polygon
    color = pineal.Color
    while window("asd").is_open():
        p = polygon(4)
        p.fill(color(0, 1, 1))
        p.stroke(color(0, 1, 0))
        p.line(10)

        w = window("asd")
        w.render(p)


if __name__ == "__main__":
    test_color()
