import pyglet.gl as gl
from core.entities import Entity
from core.shapes import solid_polygon, wired_polygon


class psolid(Entity):
    memo = {}

    def setup(self, n):
        self.n = n

    def draw(self, color):
        n = self.n

        if n not in self.memo:
            self.memo[n] = solid_polygon(n)

        vlist = self.memo[n]
        vlist.colors = color * (n * 3)
        vlist.draw(gl.GL_TRIANGLES)


class pwired(Entity):
    memo = {}

    def setup(self, n):
        self.n = n

    def draw(self, color):
        n = self.n

        if n not in self.memo:
            self.memo[n] = wired_polygon(n)

        vlist = self.memo[n]
        vlist.colors = color * n
        vlist.draw(gl.GL_LINE_LOOP)
