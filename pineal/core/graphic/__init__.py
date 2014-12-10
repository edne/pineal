import windows


class Graphic:
    def __init__(self, visuals):
        windows.init(visuals)

    def update(self):
        #dt = pyglet.clock.tick()
        windows.update()

    def run(self):
        try:
            while True:
                self.update()
        except KeyboardInterrupt:
            pass
