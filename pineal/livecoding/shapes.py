from imports import *

ezc_shapes = ezpyinline.C(
r"""
    #include <GL/freeglut.h>
    #include <math.h>

    void cube(
        double r,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glColor4f(fr, fg, fb, fa);
        glutSolidCube(r);
        glColor4f(sr, sg, sb, sa);
        glutWireCube(r);
    }

    void tetrahedron(
        double r,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glPushMatrix();
        glScalef(r,r,r);

        glColor4f(fr, fg, fb, fa);
        glutSolidTetrahedron();
        glColor4f(sr, sg, sb, sa);
        glutWireTetrahedron();
        glPopMatrix();
    }

    void dodecahedron(
        double r,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glPushMatrix();
        glScalef(r,r,r);

        glColor4f(fr, fg, fb, fa);
        glutSolidDodecahedron();
        glColor4f(sr, sg, sb, sa);
        glutWireDodecahedron();
        glPopMatrix();
    }

    void octahedron(
        double r,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glPushMatrix();
        glScalef(r,r,r);

        glColor4f(fr, fg, fb, fa);
        glutSolidOctahedron();
        glColor4f(sr, sg, sb, sa);
        glutWireOctahedron();
        glPopMatrix();
    }

    void quad(
        double l,
        double x, double y, double z,
        double fr, double fg, double fb, double fa,
        double sr, double sg, double sb, double sa
    )
    {
        glColor4f(fr,fg,fb, fa);
        glBegin(GL_POLYGON);
        glVertex3f(x-l/2, y-l/2, z);
        glVertex3f(x-l/2, y+l/2, z);
        glVertex3f(x+l/2, y+l/2, z);
        glVertex3f(x+l/2, y-l/2, z);
        glEnd();

        glColor4f(sr,sg,sb, sa);
        glBegin(GL_LINE_LOOP);
        glVertex3f(x-l/2, y-l/2, z);
        glVertex3f(x-l/2, y+l/2, z);
        glVertex3f(x+l/2, y+l/2, z);
        glVertex3f(x+l/2, y-l/2, z);
        glEnd();
    }
""")


def cube(r=1):
    f = fill(); s = stroke()
    ezc_shapes.cube(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)

def tetrahedron(r=1):
    f = fill(); s = stroke()
    ezc_shapes.tetrahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)

def dodecahedron(r=1):
    f = fill(); s = stroke()
    ezc_shapes.dodecahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)

def octahedron(r=1):
    f = fill(); s = stroke()
    ezc_shapes.octahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)

class Shape(object):
    def __init__(self):
        self._v = list()

    def vertex(self, x,y, z=0):
        self._v.append( (x,y,z) )

    def _draw(self):
        f = fill(); s = stroke()

        glColor4f(f.r,f.g,f.b, f.a)
        glBegin(GL_POLYGON)
        for v in self._v:
            glVertex3f(v[0],v[1],v[2])
        glEnd()

        glColor4f(s.r,s.g,s.b, s.a)
        glBegin(GL_LINE_LOOP)
        for v in self._v:
            glVertex3f(v[0],v[1],v[2])
        glEnd()

def createShape():
    return Shape()

def shape(s):
    s._draw()

def quad(l=1.0, x=0, y=0, z=0):
    f = fill(); s = stroke()
    ezc_shapes.quad(l,x,y,z, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def _quad(l=1.0, x=0, y=0, z=0):
    f = fill(); s = stroke()
    l = float(l)

    glColor4f(f.r,f.g,f.b, f.a)
    glBegin(GL_POLYGON)
    glVertex3f(x-l/2, y-l/2, z)
    glVertex3f(x-l/2, y+l/2, z)
    glVertex3f(x+l/2, y+l/2, z)
    glVertex3f(x+l/2, y-l/2, z)
    glEnd()

    glColor4f(s.r,s.g,s.b, s.a)
    glBegin(GL_LINE_LOOP)
    glVertex3f(x-l/2, y-l/2, z)
    glVertex3f(x-l/2, y+l/2, z)
    glVertex3f(x+l/2, y+l/2, z)
    glVertex3f(x+l/2, y-l/2, z)
    glEnd()
