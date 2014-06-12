from imports import *
import colorsys
import graphic

_color_mode = "rgb"

def colorMode(mode):
    global _color_mode
    _color_mode = mode

class Color(object):
    def __init__(self, *argv):
        if len(argv) in [1,2]:  # single or single+alpha
            if _color_mode=="rgb":
                self.r, self.g, self.b = [argv[0]]*3
            if _color_mode=="hsv":
                self.r, self.g, self.b = colorsys.hsv_to_rgb(argv[0],1,1)
            self.a = argv[1] if len(argv)==2 else 1

        elif len(argv) in [3,4]:  # 3 or 3+alpha
            if _color_mode=="rgb":
                self.r, self.g, self.b = argv[:3]
            if _color_mode=="hsv":
                self.r, self.g, self.b = colorsys.hsv_to_rgb(
                    argv[0],argv[1],argv[2]
                )
            self.a = argv[3] if len(argv)==4 else 1

    @property
    def h(self):
        return colorsys.rgb_to_hsv(self.r,self.g,self.b)[0]
    @h.setter
    def h(self, _h):
        self.r, self.g, self.b = colorsys.hsv_to_rgb(_h,self.s,self.v)

    @property
    def s(self):
        return colorsys.rgb_to_hsv(self.r,self.g,self.b)[1]
    @s.setter
    def s(self, _s):
        self.r, self.g, self.b = colorsys.hsv_to_rgb(self.h,_s,self.v)

    @property
    def v(self):
        return colorsys.rgb_to_hsv(self.r,self.g,self.b)[2]
    @v.setter
    def v(self, _v):
        self.r, self.g, self.b = colorsys.hsv_to_rgb(self.h,self.s,_v)

_fill = Color(0)
_stroke = Color(1)

def fill(*argv):
    global _fill
    if len(argv)==0:
        return _fill

    if len(argv)==1 and isinstance(argv[0], Color):
        _fill = argv[0]
    else:
        _fill = Color(*argv)

def stroke(*argv):
    global _stroke
    if len(argv)==0:
        return _stroke

    if len(argv)==1 and isinstance(argv[0], Color):
        _stroke = argv[0]
    else:
        _stroke = Color(*argv)

def noFill():
    _fill.a = 0.0

def noStroke():
    _fill.a = 0.0

def lerpColor(c1, c2, amt):
    r = c1.r*amt + c2.r*(1-amt)
    g = c1.g*amt + c2.g*(1-amt)
    b = c1.b*amt + c2.b*(1-amt)
    a = c1.a*amt + c2.a*(1-amt)
    return Color(r,g,b,a)
