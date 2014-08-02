from pineal.livecoding import *
var = {
    "alpha" : 1.0,
    "rad" : 1.0,
}


def loop():
    #rotate(0,dt/8)
    #rotate(high()/8)

    colorMode("hsv")

    h = note()
    fill(h,1,1,0.05)
    #noStroke()

    colorMode("rgb")
    stroke(noise()*bass()*4)
    strokeWeight(2)

    colorMode("hsv")

    pushMatrix()
    l = (0.5 + amp()+bass())*rad
    for i in xrange(10):
        rotate((time/10)%(2*pi))

        fill(h,1,1,0.05*amp() + 0.5)
        cube(rad*(l+sin(time+i)))

        l *= 0.9
        strokeWeight(l+0.7)
        rotate(pi/4)
        h += 0.01
    popMatrix()
