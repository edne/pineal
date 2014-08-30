from color import fill, stroke
import thirdparty.ezpyinline as ezpyinline


with open('pineal/livecoding/c/solids.c') as f:
    _ezc = ezpyinline.C(f.read())


def cube(r=1):
    f = fill()
    s = stroke()
    _ezc.cube(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def tetrahedron(r=1):
    f = fill()
    s = stroke()
    _ezc.tetrahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def dodecahedron(r=1):
    f = fill()
    s = stroke()
    _ezc.dodecahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)


def octahedron(r=1):
    f = fill()
    s = stroke()
    _ezc.octahedron(r, f.r,f.g,f.b,f.a, s.r,s.g,s.b,s.a)
