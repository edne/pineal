from imports import *
from shapes import *

class Ring(Shape):
    """
    draw a shape on the vertexes of a regular polygon
    @ivar shape: the shape to draw
    @ivar n: number of vertexes
    """
    def __init__(self, shape, n):
        self.shape = shape
        self.n = n
        Shape.__init__(self)

    def draw(self):
        push()

        rotate(self.ang - pi/2)

        push()
        for i in xrange(self.ni):
            self.before(i)
            for j in xrange(self.n):
                push()
                translate(self.r, 0)
                self.shape.draw()
                pop()
                rotate(2*pi/self.n)

            self.after(i)
        pop()

        pop()

class Grid(Shape):
    def __init__(self, shape, l=1,m=1,n=1):
        self.shape = shape
        self.l,self.m,self.n = l,m,n
        Shape.__init__(self)

    def draw(self):
        push()

        for iteration in xrange(self.ni):
            self.before(iteration)

            for i in xrange(self.l):
                for j in xrange(self.m):
                    for k in xrange(self.n):
                        push()
                        translate(
                            (i-float(self.l-1)/2)*float(self.r)/self.l,
                            (j-float(self.m-1)/2)*float(self.r)/self.m,
                            (k-float(self.n-1)/2)*float(self.r)/self.n,
                        )
                        self.shape.draw()
                        pop()

            self.after(iteration)

        pop()
