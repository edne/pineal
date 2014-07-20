from random import uniform
import pyglet.gl as gl

import thirdparty.ezpyinline as ezpyinline
from pineal import analyzer


def _vec(*args):
    return (gl.GLfloat * len(args))(*args)


_ezc_utils = ezpyinline.C(r"""
    #include <GL/freeglut.h>
    #include <math.h>

    void rotate(double angx, double angy, double angz)
    {
        glRotatef(180.0*angx/M_PI, 1,0,0);
        glRotatef(180.0*angy/M_PI, 0,1,0);
        glRotatef(180.0*angz/M_PI, 0,0,1);
    }

    void translate(double x, double y, double z)
    {
        glTranslatef(x, y, z);
    }

    void scale(double x, double y, double z)
    {
        glScalef(x, y, z);
    }

    void push(void)
    {
        glPushMatrix();
    }

    void pop(void)
    {
        glPopMatrix();
    }
""")


def strokeWeight(w):
    gl.glLineWidth(w)


def rotateX(angle):
    rotate(angx = angle)


def rotateY(angle):
    rotate(angy = angle)


def rotateZ(angle):
    rotate(angz = angle)


def rotate(angz=0, angy=0, angx=0):
    _ezc_utils.rotate(angx,angy,angz)


def translate(x=0, y=0, z=0):
    _ezc_utils.translate(x, y, z)


def scale(x, y=None, z=1):
    if not y:
        y = x
    _ezc_utils.scale(x, y, z)

_matrix_stack = 0


def pushMatrix():
    global _matrix_stack
    if _matrix_stack<30:
        _ezc_utils.push()
        _matrix_stack += 1
    else:
        print "TOO many push()"
        raise Exception()


def popMatrix():
    global _matrix_stack
    if _matrix_stack>0:
        _ezc_utils.pop()
    else:
        print "TOO many pop()"
        raise Exception()
    _matrix_stack -= 1 # if goes to -1 i can handle it


def resetMatrix():
    global _matrix_stack
    _matrix_stack = 0
    gl.glLoadIdentity()


def random(a=0, b=1):
    """ uniform distribution """
    return uniform(a,b)


def noise(a=1):
    """ white noise (uniform distribution in [-a,+a]) """
    return uniform(-a,a)


def band(a, b=None):
    return analyzer.band(a,b)


# light
def ambient(amb):
    """ set ambiental light intensity """
    gl.glLightModelfv(
        gl.GL_LIGHT_MODEL_AMBIENT|gl.GL_LIGHT_MODEL_TWO_SIDE,
        _vec(amb,amb,amb, 1.0)
    )


def light(val):
    """ set light intensity """
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, _vec(val, val, val, 1.0))


def light_pos(x,y,z):
    """ set light position """
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, _vec(x,y,z, 3))
#
