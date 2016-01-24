from __future__ import print_function
import os
from time import time, sleep


def test_dsl():
    "Test DSL"
    from pineal.visions import load

    v = load("test/test_lisp.hy")

    start_time = time()
    while time() < start_time + 1:
        v.loop()
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
        f.write("(+ 1 1)")

    v = load("temp.hy")

    sleep(1)
    assert v.loop() == 2

    with open("temp.hy", "w") as f:
        f.write("(+ 1 2)")

    sleep(1)
    assert v.loop() == 3

    v.stop()
    v.join()

    os.remove("temp.hy")
