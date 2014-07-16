from pineal.livecoding import *
var = {
    "alpha" : 1.0,
    "rad" : 1.0,
}

def loop():

    rotate(dt/2)

    colorMode("hsv")

    h = note()+0.4
    fill(h,1,1,0.05)
    #noStroke()

    colorMode("rgb")
    stroke(0.8)
    strokeWeight(2)

    f = fill();
    #s = stroke()
    glColor4f(f.r,f.g,f.b, f.a)

    colorMode("hsv")

    pushMatrix()
    l = 2.0
    for i in xrange(50):
        rotate((time/10)%(2*pi))

        fill(h,1,1,0.05)
        quad(l)

        l *= 0.9
        strokeWeight(l+0.7)
        rotate(bass()+pi/4)
        h += 0.01
    popMatrix()
