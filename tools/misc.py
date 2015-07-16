from time import time
from math import pi


def time2rad(mult=1):
    return (time() * mult) % pi
