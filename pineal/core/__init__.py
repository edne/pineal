from threading import Thread
from visuals import Visual
from graphic import Graphic

from pineal.osc import Osc
from pineal.config import OSC_CORE, OSC_GUI

import pineal.livecoding.audio


class Core(Thread):
    """Run visuals and show them in Overview and Master windows"""
    def __init__(self):
        Thread.__init__(self)
        self.visuals = {}
        self.osc = Osc(OSC_CORE, OSC_GUI)

        self.osc.listen('visual', self.cb_visual)
        self.osc.listen('audio', self.cb_audio)
        self.osc.listen('code', self.cb_code)

    def run(self):
        print 'starting pineal.core'
        self.osc.start()
        self.graphic = Graphic(self.visuals)
        self.graphic.run()
        self.osc.stop()

    def stop(self):
        self.graphic.stop()

    def cb_visual(self, path, tags, args, source):
        path = [s for s in path.split('/') if s]
        value = (args if tags[1:] else args[0]) if args else None
        visual, var = path[1:]

        self.visuals[visual][var] = value

    def cb_audio(self, path, tags, args, source):
        path = [s for s in path.split('/') if s]
        value = (args if tags[1:] else args[0]) if args else None
        key, = path[1:]

        pineal.livecoding.audio.__dict__[key] = value

    def cb_code(self, path, tags, args, source):
        name = [s for s in path.split('/') if s][1]
        code = args[0]

        # TODO replace that
        if name not in self.visuals.keys():
            self.visuals[name] = Visual(self, name)
        #
        self.visuals[name].load(code)
