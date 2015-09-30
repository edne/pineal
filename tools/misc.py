from time import time as _time
from math import pi, sqrt


sqrt_2 = sqrt(2)


def time_rad(mult=1, add=0):
    return (time() * mult + add) % (2*pi)


def time(mult=1, add=0):
    return _time() * mult + add
