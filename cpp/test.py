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
    polygon = pineal.Polygon.memo

    while window("asd").is_open():
        window("asd").display(polygon(4))


if __name__ == "__main__":
    test_child()
