from imports import *

sys.path.insert(0, 'thirdparty/mattrobenolt/colors.py')
import colors

class Color:
    def __init__(self, *argl, **argd):
        self.r = 0.0
        self.g = 0.0
        self.b = 0.0
        self.a = 1.0

        if len(argl)==1:  # greyscale
            self.r = self.g = self.b = argl[0]

        if len(argl)==3:
            self.r, self.g, self.b = argl
            self.a = 1.0

        if len(argl)==4:
            self.r, self.g, self.b, self.a = argl

        for key in argd:
            if key in self.__dict__:
                self.__dict__[key] = argd[key]
            #if '_'+key in self.__dict__:
            #    self.__dict__['_'+key] = argd[key]

    #@property
    #def h(self):
        #return colors.rgb(self.r, self.g, self.b).hsv
        #return colors.rgb

    #@h.setter
    #def h(self, value):
    #    None
