
class Visuals(dict):
    def new(self, name):
        v = Visual(self, name)
        self[name] = v
        return v


class Visual():
    def __init__(self, visuals, name):
        self.visuals = visuals
        print 'creating visual'
        self.name = name
        self._stack = list()
        self.box = Box()
        self.osc = {}

    def load(self, code):
        self._stack.append(code)

    def remove(self):
        del self.visuals[self.name]

    def update(self):
        if not self._stack:
            return

        try:
            variables = self.box.__dict__.copy()
            exec(self._stack[-1], self.box.__dict__)
            for k,v in variables.items():
                if not callable(v) and k in self.box.__dict__.keys():
                    self.box.__dict__[k] = v
            self.loop()
        except Exception as e:
            print self.error_log(e)

            self._stack = self._stack[:-1]
            if not self._stack:
                print "%s.py is BROKEN" % self.name
            else:
                self.update() # WARNING recursion!

    def get_var(self):
        d = self.box.__dict__
        return [k for k in d.keys() if isinstance(d[k], float)]

    def set_var(self, var, value):
        self.osc[var] = value

    def error_log(self, e):
        log = self.name + '.py'
        log += str(e)

        if hasattr(e, 'text'):
            log += "\n"+str(e.text)

        return log

    def loop(self):
        for k in self.get_var():
            if k not in self.osc.keys():
                self.osc[k] = self.box.__dict__[k]

        for k in self.osc.keys():
            if k in self.get_var():
                # if osc[] is changed:
                self.box.__dict__[k] = self.osc[k]
                # elif values are changed:
                #   update osc[] with new values
            else:
                del self.osc[k]

        self.box.loop()


class Box(object):
    def loop(self):
        None
