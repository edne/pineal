from time import time as _time
from math import *

from core.nerve import get_source


def time_rad(mult=1, add=0):
    return (time() * mult + add) % pi


def time(mult=1, add=0):
    return _time() * mult + add
