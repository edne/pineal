from imports import *

import numpy as np
import math
from scipy import weave

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

ezc_rotate = ezpyinline.C(
r"""
    #include <GL/freeglut.h>
    #include <math.h>

    void rotate(double angx, double angy, double angz)
    {
        glRotatef(180.0*angx/M_PI, 1,0,0);
        glRotatef(180.0*angy/M_PI, 0,1,0);
        glRotatef(180.0*angz/M_PI, 0,0,1);
    }
""")
def rotate(angz=0, angy=0, angx=0):
    ezc_rotate.rotate(angx,angy,angz)

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
