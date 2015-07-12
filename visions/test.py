from lib.graphic import *
from math import *
from random import *

from lib.audio import amp, bass, high


def draw():
    strokeWeight(5)

    do(
        scale(amp()),
        pwired(4)(rgb(1)),
    )()
