import OpenGL.GLUT as glut
from windows import Output


class Graphic:
    def __init__(self, visuals):
        glut.glutInit([])
        self.output = Output(visuals)

    def run(self):
        try:
            while True:
                self.output.update()
        except KeyboardInterrupt:
            pass
