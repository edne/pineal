from __future__ import print_function
import os
from time import time, sleep


def _test_python():
    "Test Python APIs"
    from math import pi
    import pineal

    polygon = pineal.Polygon
    color = pineal.Color
    signal = pineal.Signal

    start_time = time()
    while time() < start_time + 1:
        p1 = polygon(4)
        p2 = polygon(8)
        p3 = polygon(3)

        g = pineal.Group()
        g.add(p1)
        g.add(p2)

        t = pineal.Group()
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

        l = pineal.Layer.memo("lv1")
        l.render(t)

        w = pineal.Window.memo("asd")
        if w.is_open():
            w.render(pineal.Layer.memo("lv1"))
    # TODO close window


def test_dsl():
    "Test DSL"
    import hy
    from test_lisp import loop

    start_time = time()
    while time() < start_time + 1:
        loop()
    # TODO close window


def test_watcher():
    "Test the file watching util"
    from pineal.utils import watch_file

    with open("temp_file", "w") as f:
        f.write("before")

    status = ["a"]

    def action():
        status[0] = "b"

    watcher = watch_file("temp_file", action)

    with open("temp_file", "w") as f:
        f.write("after")

    sleep(1)
    assert status[0] == "b"

    watcher.stop()
    watcher.join()

    os.remove("temp_file")


def test_vision():
    "Test loading and changeing of a vision"
    from pineal.visions import load

    with open("temp.hy", "w") as f:
        f.write("(defn loop [] (+ 1 1))")

    v = load("temp.hy")

    sleep(1)
    assert v.loop() == 2

    with open("temp.hy", "w") as f:
        f.write("(defn loop [] (+ 1 2))")

    sleep(1)
    assert v.loop() == 3

    v.stop()
    v.join()

    os.remove("temp.hy")
