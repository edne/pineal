from math import pi
import pyglet.gl as gl
from pineal.matrix import push, pop


def translate(x, y=0.0, z=0.0):
    def effect(entity):
        push()
        gl.glTranslatef(x, y, z)
        entity()
        pop()

    return effect


def scale(*args):
    def effect(entity):
        if len(args) == 3:
            x, y, z = args
        elif len(args) == 2:
            x, y, z = args + [1]
        elif len(args) == 1:
            x, y, z = args * 3
        else:
            raise TypeError  # TODO better explaination
        push()
        gl.glScalef(x, y, z)
        entity()
        pop()

    return effect


def rotate(angle,
           x=0.0, y=0.0, z=1.0):
    def effect(entity):
        push()
        gl.glRotatef(angle * 180 / pi,
                     x, y, z)
        entity()
        pop()

    return effect


def turnaround(n):
    def effect(entity):
        rs = [0.0]

        for i in range(n):
            push()
            angle = 2.0 * pi * i / n
            gl.glRotatef(angle * 180 / pi,
                         0, 0, 1)
            for r in rs:
                gl.glTranslatef(r, 0.0, 0.0)
                entity()
            pop()

    return effect
