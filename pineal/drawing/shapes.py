from imports import *

class Shape(object):
    _before = ""
    _solid = ""
    _wire  = ""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 1

        self._fill = None
        self._stroke = (1,1,1,1)

    def fill(self, c, a=1):
        self._fill = (c.r, c.g, c.b, a)
    def stroke(self, c, a=1):
        self._stroke = (c.r, c.g, c.b, a)

    def noFill(self):
        self._fill = None
    def noStroke(self):
        self._stroke = None

    def draw(self):
        x, y, z = self.x, self.y, self.z
        r = self.r

        fill = int(bool(self._fill))
        stroke = int(bool(self._stroke))

        fr,fg,fb,fa = self._fill
        sr,sg,sb,sa = self._stroke

        if hasattr(self, "_vertex"):
            vertex = self._vertex.ctypes.data
            nv = len(self._vertex)

        support = "#include <GL/freeglut.h>"
        code = """
            glPushMatrix();
            glTranslatef(x, y, z);
            %s // before
            if(fill)
            {
                glColor4f(fr,fg,fb, fa);
                %s  // solid
            }
            if(stroke)
            {
                glColor4f(sr,sg,sb, sa);
                %s  // wire
            }
            glPopMatrix();
        """ % (self._before, self._solid, self._wire)

        weave.inline(
            code,
            locals().keys(),
            support_code = support,
            libraries = ['GL','glut','GLU']
        )

class Polygon(Shape):
    _before = """
        glVertexPointer( 2, GL_DOUBLE, 0, (GLvoid*)vertex);
        glScalef(r, r, r);
    """
    _wire = "glDrawArrays( GL_LINE_LOOP, 0, nv );"

    def __init__(self, *vertex):
        vertex = list(vertex)
        vertex.append(vertex[0])
        self._vertex = np.array(vertex)
        Shape.__init__(self)

class Regular(Polygon):
    def __init__(self, n):
        self.n = n

        vx = np.cos(np.linspace(0,2*pi, self.n+1))[:-1]
        vy = np.sin(np.linspace(0,2*pi, self.n+1))[:-1]
        vertex = np.column_stack((vx,vy))

        Polygon.__init__(self, *vertex)

class Circle(Regular):
    def __init__(self):
        Regular.__init__(self, 30)


class GlutPreset(Shape):
    None

class Cube(GlutPreset):
    _solid = "glutSolidCube(r);"
    _wire  = "glutWireCube(r);"

class Sphere(GlutPreset):
    _solid = "glutSolidSphere(r, 10, 10);"
    _wire  = "glutWireSphere(r, 10, 10);"

class Tetrahedron(GlutPreset):
    _before ="glScalef(r,r,r);"
    _solid = "glutSolidTetrahedron();"
    _wire  = "glutWireTetrahedron();"

class Dodecahedron(GlutPreset):
    _before ="glScalef(r,r,r);"
    _solid = "glutSolidDodecahedron();"
    _wire  = "glutWireDodecahedron();"

class Octahedron(GlutPreset):
    _before ="glScalef(r,r,r);"
    _solid = "glutSolidOctahedron();"
    _wire  = "glutWireOctahedron();"

class Icosahedron(GlutPreset):
    _before ="glScalef(r,r,r);"
    _solid = "glutSolidIcosahedron();"
    _wire  = "glutWireIcosahedron();"

#class Teapot(GlutPreset):
#    _solid = "glutSolidTeapot(r);"
#    _wire  = "glutWireTeapot(r);"
