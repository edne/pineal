from time import time
from math import *

from core.nerve import get_source


def time2rad(mult=1):
    return (time() * mult) % pi
