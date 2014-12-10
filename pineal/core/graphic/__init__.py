import OpenGL.GLUT as glut
from windows import Output


class Graphic:
    def __init__(self, visuals):
        glut.glutInit([])
        self.output = Output(visuals)
        self._stop = False

    def run(self):
        try:
            while not self._stop:
                self.output.update()
        except KeyboardInterrupt:
            pass

    def stop(self):
        self._stop = True
