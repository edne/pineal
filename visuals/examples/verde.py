from pineal.livecoding import *
var = {
    "alpha" : 1.0,
    "rad" : 1.0,
}

def loop():
    colorMode("hsv")

    h = note()+0.3
    fill(h,1,1,1)
    #noStroke()

    colorMode("rgb")
    stroke(0)
    strokeWeight(2)

    f = fill();
    #s = stroke()
    glColor4f(f.r,f.g,f.b, f.a)

    colorMode("hsv")

    pushMatrix()
    l = 1.0
    #rotate((time/10)%(2*pi))

    fill(h,1,1,0.1)
    n = 10
    l = 1.0
    r = 0.5
    pushMatrix()
    
    for i in xrange(4):
        fill(h+0.1*i,1,1,0.1)
        for j in xrange(n):
            rotate(2*pi/n)
            rotate((time/10)%(2*pi), (time/5)%(2*pi))
            translate(r)
            quad(l)
            translate(-r)
        r *= 0.6
        l *= 0.4

    popMatrix()

    l *= 0.9
    strokeWeight(l+0.7)
    rotate(bass()+pi/4)
    h += 0.01
    popMatrix()
