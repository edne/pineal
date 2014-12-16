from lib.graphic import Square

square = Square()
bass = 0


def setup():
    pass


def draw():
    square.side = 1 + bass*8
    square.draw()
