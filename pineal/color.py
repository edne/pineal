from imports import *

sys.path.insert(0, 'thirdparty/mattrobenolt/colors.py')
import colors

class Color:
    def __init__(self, *argl, **argd):
        self.r = 0.0
        self.g = 0.0
        self.b = 0.0

        if len(argl)==1:
            self.r = self.g = self.b = argl[0]
