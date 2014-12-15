from color import fill, stroke
import thirdparty.ezpyinline as ezpyinline


with open('livecoding/c/shapes.c') as f:
    _ezc = ezpyinline.C(f.read())


def square(l=1.0, x=0, y=0, z=0):
    f = fill()
    s = stroke()
    _ezc.square(l,x,y,z, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)
