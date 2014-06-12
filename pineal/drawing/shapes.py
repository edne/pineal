from imports import *

def gen_inline(out="", before="", solid="", wire=""):
    code = r"""
        #include <GL/freeglut.h>
        %s
        void draw(
            double x, double y, double z,
            double r,
            int fill, int stroke,
            double fr, double fg, double fb, double fa,
            double sr, double sg, double sb, double sa
        )
        {
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
        }
    """ % (out, before, solid, wire)

    ezc = ezpyinline.C(code)
    return ezc

class Shape(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.r = 1

    @property
    def center(self):
        return (self.x, self.y, self.z)

    @center.setter
    def center(self, (x,y,z)):
        (self.x, self.y, self.z) = (x,y,z)

    def draw(self):
        f = fill()
        s = stroke()
        self.inline.draw(
            self.x, self.y, self.z,
            self.r,
            int(f.a!=0.0), int(s.a!=0.0),
            f.r, f.g, f.b, f.a,
            s.r, s.g, s.b, s.a
        )

class Polygon(Shape):
    inline = gen_inline(
        out ="""
            int nv;
            void init(int n, int vertex)
            {
                nv = n;
                glVertexPointer( 2, GL_DOUBLE, 0, (GLvoid*)vertex);
            }
        """,
        before="glScalef(r, r, r);",
        solid="glDrawArrays( GL_POLYGON, 0, nv );",
        wire ="glDrawArrays( GL_LINE_LOOP, 0, nv );"
    )

    def __init__(self, *vertex):
        vertex = list(vertex)
        vertex.append(vertex[0])
        self._vertex = np.array(vertex)
        Shape.__init__(self)

    def draw(self):
        self.inline.init(len(self._vertex), self._vertex.ctypes.data)
        Shape.draw(self)

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
    inline = gen_inline(
        solid="glutSolidCube(r);",
        wire ="glutWireCube(r);"
    )

class Sphere(GlutPreset):
    inline = gen_inline(
        solid="glutSolidSphere(r, 10, 10);",
        wire ="glutWireSphere(r, 10, 10);"
    )

class Tetrahedron(GlutPreset):
    inline = gen_inline(
        before="glScalef(r,r,r);",
        solid ="glutSolidTetrahedron();",
        wire  ="glutWireTetrahedron();"
    )

class Dodecahedron(GlutPreset):
        inline = gen_inline(
            before="glScalef(r,r,r);",
            solid ="glutSolidDodecahedron();",
            wire  ="glutWireDodecahedron();"
        )

class Octahedron(GlutPreset):
        inline = gen_inline(
            before="glScalef(r,r,r);",
            solid ="glutSolidOctahedron();",
            wire  ="glutWireOctahedron();"
        )

class Icosahedron(GlutPreset):
        inline = gen_inline(
            before="glScalef(r,r,r);",
            solid ="glutSolidIcosahedron();",
            wire  ="glutWireIcosahedron();"
        )
