from pyglet.gl import *


class Entity(object):
    vertsGl = None

    @staticmethod
    def _generateVerts():
        verts = []

        Entity.vertsGl = (GLfloat * len(verts))(*verts)

    def __init__(self, side=1.0):
        self.side = side
        self.color = (0,1,1)

    def draw(self):
        glLoadIdentity()
        glScalef(self.side, self.side, 1)
        glColor3f(1, 1, 1)

        glVertexPointer(2, GL_FLOAT, 0, self.vertsGl)

        glEnableClientState(GL_VERTEX_ARRAY)
        glPolygonMode( GL_FRONT, GL_LINE )
        glDrawArrays(GL_QUADS, 0, len(self.vertsGl) // 2)


class Square(Entity):
    @staticmethod
    def _generateVerts():
        verts = [
            -1,-1,
            1, -1,
            1,  1,
            -1, 1]
        Square.vertsGl = (GLfloat * len(verts))(*verts)


Entity._generateVerts()
Square._generateVerts()
