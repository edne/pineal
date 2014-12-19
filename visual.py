import hy


class Visual(object):
    class Box(object):
        def setup(self):
            pass

        def draw(self):
            pass

    def __init__(self, name, code):
        self.name = name

        print 'creating visual'
        self._stack = list()
        self.box = Visual.Box()

        self.load(code)

    def load(self, code):
        try:
            exec(code, self.box.__dict__)
            self.box.setup()
            self._stack.append(code)
        except Exception as e:
            print(e)

    def iteration(self):
        if not self._stack:
            return

        try:
            self.box.draw()
        except Exception as e:
            print(e)
            self._stack = self._stack[:-1]
            if not self._stack:
                print "%s.py is BROKEN" % self.name
            else:
                self.iteration()
