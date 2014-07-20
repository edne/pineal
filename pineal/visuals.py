import time

l = []


def init():
    global l
    l = []


#def add(v):
#    l.append(v)


def new(name):
    v = Visual(name)
    l.append(v)
    return v


def remove(v):
    l.remove(v)
    del v


def get(name=''):
    if name:
        for v in l:
            if name == v.name:
                return v
        return None
    else:
        return l


def names():
    for v in get():
        yield v.name


class Visual():
    def __init__(self, name):
        print 'creating visual'
        self.name = name
        self._stack = list()
        self.box = Box()

    def load(self, code):
        self._stack.append(code)

    def remove(self):
        remove(self)

    def update(self):
        if not self._stack:
            return

        try:
            exec(self._stack[-1], self.box.__dict__)
            self.loop()
        except Exception as e:
            print self.error_log(e)

            self._stack = self._stack[:-1]
            if not self._stack:
                print "%s.py is BROKEN" % self.name
            else:
                self.update() # WARNING recursion!

    def error_log(self, e):
        log = self.name + '.py'
        log += str(e)

        if hasattr(e, 'text'):
            log += "\n"+str(e.text)

        return log

    def loop(self):
        self.box.time = time.time()
        if self.box.last_time:
            self.box.dt = self.box.last_time - self.box.time
        self.box.last_time = self.box.time

        for k in self.box.var.keys():
            if k not in self.box.__dict__.keys():
                self.box.__dict__[k] = self.box.var[k]

        self.box.loop()


class Box:
    def __init__(self):
        self.time = 0
        self.last_time = 0
        self.dt = 0

        self.var = dict()

    def loop(self):
        None


def reciver(name, key, value):
    for v in get():
        if name=="*" or name==v.name:
            v.box.__dict__[key] = value  # this is NOT safe (if used with OSC)
