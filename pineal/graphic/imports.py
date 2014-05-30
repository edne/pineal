from pineal.imports import *
from pineal import visuals

from OpenGL.GLUT import *
import pyglet
from pyglet.gl import *
from thirdparty.shader import Shader

import thirdparty.ezpyinline as ezpyinline

from pyglet.window import mouse
from pyglet.window import key

def vec(*args):
	return (GLfloat * len(args))(*args)

import camera, windows
