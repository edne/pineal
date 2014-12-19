from time import time
from inspect import isclass
import pineal.livecoding


class Visuals(dict):
    def __init__(self, core):
        dict.__init__(self)
        self.core = core

    def new(self, name):
        v = Visual(self.core, name)
        self[name] = v
        return v


class Visual(dict):
    def __init__(self, core, name):
        dict.__init__(self)
        self.core = core
        self.name = name

        print 'creating visual'
        self._stack = list()
        self.box = Box()
        self.lastTime = time()

    def load(self, code):
        self._stack.append(code)

    def iteration(self):
        if not self._stack:
            return

        #self.core.osc.send('error', self.name, '')
        try:
            stored = self.box.__dict__.copy()         # make a copy
            exec self._stack[-1] in self.box.__dict__
            self.box.__dict__.update({                # restore old values
                k: v
                for k,v in stored.items()
                if not callable(v) and not isclass(v) # but only for variables
            })
            self.loop()  # finally try to run main iteration
        except Exception as e:
            print self.error_log(e)
            self.core.osc.send('error', self.name, str(e))

            self._stack = self._stack[:-1]
            if not self._stack:
                print "%s.py is BROKEN" % self.name
            else:
                self.iteration()

        d = self.box.__dict__
        added = {  # float vairiables not stored
            k: v
            for k,v in d.items()
            if isinstance(v, float) and k!='dt' and k not in stored.keys()
        }
        for (var, value) in added.items():
            self.core.osc.send('add', self.name, var, value)
        self.update(added)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.box.__dict__[key] = value

    def error_log(self, e):
        log = self.name + '.py'
        log += str(e)

        if hasattr(e, 'text'):
            log += "\n"+str(e.text)

        return log

    def loop(self):
        pineal.livecoding.__dict__['dt'] = time() - self.lastTime
        self.lastTime = time()

        self.box.loop()


class Box(object):
    def loop(self):
        None
