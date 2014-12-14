#!/usr/bin/env python

from threading import Thread
from lib.graphic import Graphic

import hy
from lib.osc import Osc
from config import OSC_EYE

import livecoding.audio


class Eye(Thread):
    """Run visuals and show them in Overview and Master windows"""
    def __init__(self):
        Thread.__init__(self)
        self.visuals = {}
        self.osc = Osc()
        self.osc.reciver(OSC_EYE)

    def run(self):
        print('starting eye.py')

        self.osc.listen('/ear', self.audio)
        self.osc.listen('/visual/new', self.new)

        self.osc.start()
        self.graphic = Graphic(self.visuals)
        self.graphic.run()

        print('\rstopping eye.py')
        self.osc.stop()

    def stop(self):
        self.graphic.stop()

    def audio(self, path, args):
        livecoding.audio.__dict__[args[0]] = args[1]

    def new(self, path, args):
        name, code = args
        self.visuals[name] = Visual(name, code)


class Visual(dict):
    class Box(object):
        def loop(self):
            None

    def __init__(self, name, code):
        dict.__init__(self)
        self.name = name

        print 'creating visual'
        self._stack = list()
        self.box = Visual.Box()

        self.load(code)

    def load(self, code):
        self._stack.append(code)

    def iteration(self):
        if not self._stack:
            return

        try:
            exec(self._stack[-1], self.box.__dict__)
            self.loop()
        except Exception:
            self._stack = self._stack[:-1]
            if not self._stack:
                print "%s.py is BROKEN" % self.name
            else:
                self.iteration()

    def loop(self):
        self.box.loop()


if __name__ == "__main__":
    Eye().run()
