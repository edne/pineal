from imports import *
from pineal import analyzer

import math
from scipy import weave

ezc_utils = ezpyinline.C(
r"""
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

def linew(w):
    glLineWidth(w)

def rotatex(angle):
    rotate(angx = angle)
def rotatey(angle):
    rotate(angy = angle)
def rotatez(angle):
    rotate(angz = angle)

def rotate(angz=0, angy=0, angx=0):
    ezc_utils.rotate(angx,angy,angz)

def translate(x=0, y=0, z=0):
    ezc_utils.translate(x, y, z)

def scale(ratio):
    scalexyz(ratio, ratio, ratio)

def scalexyz(rx, ry, rz):
    ezc_utils.scale(rx, ry, rz)

matrix_stack = 0
def push():
    global matrix_stack
    if matrix_stack<30:
        ezc_utils.push()
        matrix_stack += 1
    else:
        print "TOO many push()"
def pop():
    global matrix_stack
    if matrix_stack>0:
        ezc_utils.pop()
    else:
        print "TOO many pop()"
    matrix_stack -= 1 # if goes to -1 i can handle it

def identity():
    glLoadIdentity()

def random(a=0, b=1):
    """ uniform distribution """
    return uniform(a,b)

def noise(a=1):
    """ white noise (uniform distribution in [-a,+a]) """
    return uniform(-a,a)

def band(a, b=None):
    return analyzer.band(a,b)

# TODO: in C?
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
