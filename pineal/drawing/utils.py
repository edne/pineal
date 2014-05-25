from imports import *

import numpy as np
import math
from scipy import weave


def _rotation_matrix(axis, theta, mat=None):
    if not mat:
        mat = np.eye(3, 3)

    support = "#include <math.h>"
    code = """
        double x = sqrt(axis[0] * axis[0] + axis[1] * axis[1] + axis[2] * axis[2]);
        double a = cos(theta / 2.0);
        double b = -(axis[0] / x) * sin(theta / 2.0);
        double c = -(axis[1] / x) * sin(theta / 2.0);
        double d = -(axis[2] / x) * sin(theta / 2.0);

        mat[0] = a*a + b*b - c*c - d*d;
        mat[1] = 2 * (b*c - a*d);
        mat[2] = 2 * (b*d + a*c);

        mat[3*1 + 0] = 2*(b*c+a*d);
        mat[3*1 + 1] = a*a+c*c-b*b-d*d;
        mat[3*1 + 2] = 2*(c*d-a*b);

        mat[3*2 + 0] = 2*(b*d-a*c);
        mat[3*2 + 1] = 2*(c*d+a*b);
        mat[3*2 + 2] = a*a+d*d-b*b-c*c;
    """

    weave.inline(code, ['axis', 'theta', 'mat'], support_code=support, libraries=['m'])

    return mat

def rotate(v, theta, axis=np.array([0, 0, 1])):
    matrix = _rotation_matrix(axis, theta)
    return np.dot(v, matrix.T)


def time_rad(scale=1):
    """ scale time (in seconds) and mod by 2pi """
    return (time.time()*scale)%(2*pi)

def linew(w):
    """ line width """
    glLineWidth(w)


def rotatex(angle):
    rotate(angx = angle)
def rotatey(angle):
    rotate(angy = angle)
def rotatez(angle):
    rotate(angz = angle)

def rotate(angz, angy=0, angx=0):
    support = """
    #include <GL/freeglut.h>
    #include <math.h>
    """
    code = """
        glRotatef(180.0*angx/M_PI, 1,0,0);
        glRotatef(180.0*angy/M_PI, 0,1,0);
        glRotatef(180.0*angz/M_PI, 0,0,1);
    """
    weave.inline(code, ['angx','angy','angz'], support_code = support, libraries = ['GL','glut','GLU'])

def translate(x,y=0, z=0):
    glTranslatef(x, y, z)

def scale(ratio):
    scalexyz(ratio, ratio, ratio)

def scalexyz(rx, ry, rz):
    glScalef(rx, ry, rz)

def push():
    """ push the actual state in the openGL matrix stack """
    glPushMatrix()
def pop():
    """ pop the actual state in the openGL matrix stack """
    glPopMatrix()

def identity():
    """ clear applied transformations """
    glLoadIdentity()

def random(a=0, b=1):
    """ uniform distribution """
    return uniform(a,b)

def noise(a=1):
    """ white noise (uniform distribution in [-a,+a]) """
    return uniform(-a,a)

# light
def ambient(amb):
    """ set ambiental light intensity """
    glLightModelfv(
            GL_LIGHT_MODEL_AMBIENT|GL_LIGHT_MODEL_TWO_SIDE,
            vec(amb,amb,amb, 1.0)
        )
def light(val):
    """ set light intensity """
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(val, val, val, 1.0))

def light_pos(x,y,z):
    """ set light position """
    glLightfv(GL_LIGHT0, GL_POSITION, vec(x,y,z, 3))
#
