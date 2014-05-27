from imports import *
from shapes import *

class Ring(object):
    def __init__(self, n, r=1):
        self.n = n
        self.r = r
        self.i = 0

    def __iter__(self):
        self.i = 0
        return self

    def next(self):
        if self.i >= self.n:
            raise StopIteration
        else:
            ang = self.i * 2*pi/self.n
            self.i += 1
            return (
                self.r * cos(ang),
                self.r * sin(ang),
                0
            )
