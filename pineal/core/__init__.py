from threading import Thread
from visuals import Visual
from graphic import Graphic

from utils.osc import Osc
from config import OSC_CORE

import livecoding.audio


class Core(Thread):
    """Run visuals and show them in Overview and Master windows"""
    def __init__(self):
        Thread.__init__(self)
        self.visuals = {}
        self.osc = Osc()
        self.osc.reciver(OSC_CORE)

    def run(self):
        print 'starting pineal.core'

        self.osc.listen('/ear', self.cb_audio)
        self.osc.listen('/watcher/new', self.cb_code)

        self.osc.start()
        self.graphic = Graphic(self.visuals)
        self.graphic.run()
        self.osc.stop()

    def stop(self):
        self.graphic.stop()

    def cb_audio(self, path, args):
        livecoding.audio.__dict__[args[0]] = args[1]

    def cb_code(self, path, args):
        name, code = args

        # TODO replace that
        if name not in self.visuals.keys():
            self.visuals[name] = Visual(self, name)
        #
        self.visuals[name].load(code)
