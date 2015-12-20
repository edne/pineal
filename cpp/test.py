from __future__ import print_function

def test_class():
    import pineal

    win = pineal.Window("asd")

    while win.is_open():
        win.draw()


def test_memo():
    from pineal import window

    while True:
        window("asd")


if __name__ == "__main__":
    test_memo()
