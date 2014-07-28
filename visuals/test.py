from pineal.livecoding import *
var = {
    "alpha" : 1.0,
    "rad" : 1.0,
}


def loop():
    #rotate(0,dt/8)
    #rotate(high()/8)

    colorMode("hsv")

    h = note()+0.3
    fill(h,1,1,0.05)
    #noStroke()

    colorMode("rgb")
    stroke(noise()*bass()*4)
    strokeWeight(2)

    colorMode("hsv")

    pushMatrix()
    l = (1.0 + bass()*4)*rad
    for i in xrange(10):
        #rotate((time/10)%(2*pi))

        fill(h,1,1,0.05)
        tetrahedron(rad*(l+sin(time+i)))

        l *= 0.9
        strokeWeight(l+0.7)
        rotate(pi/4)
        h += 0.01
    popMatrix()
