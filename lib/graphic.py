import pyglet.gl as gl


class Entity(object):
    vertsGl = None

    @staticmethod
    def _generateVerts():
        verts = []

        Entity.vertsGl = (gl.GLfloat * len(verts))(*verts)

    def __init__(self, side=1.0):
        self.side = side
        self.color = (0,1,1)

    def draw(self):
        gl.glLoadIdentity()
        gl.glScalef(self.side, self.side, 1)
        gl.glColor3f(1, 1, 1)

        gl.glVertexPointer(2, gl.GL_FLOAT, 0, self.vertsGl)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glPolygonMode( gl.GL_FRONT, gl.GL_LINE )
        gl.glDrawArrays(gl.GL_QUADS, 0, len(self.vertsGl) // 2)


class Square(Entity):
    @staticmethod
    def _generateVerts():
        verts = [
            -1,-1,
            1, -1,
            1,  1,
            -1, 1]
        Square.vertsGl = (gl.GLfloat * len(verts))(*verts)


Entity._generateVerts()
Square._generateVerts()
