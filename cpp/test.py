from __future__ import print_function
import pineal


def test_memo():
    "Test memoizing"
    window = pineal.Window.memo

    while window("asd").is_open():
        window("asd").draw()


if __name__ == "__main__":
    test_memo()
