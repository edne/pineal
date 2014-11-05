from visuals import Visuals
from graphic import Graphic
from loader import Loader

from pineal.osc import Osc
from pineal.config import OSC_CORE, OSC_GUI

import pineal.livecoding.audio


class Core(object):
    """Run visuals and show them in Overview and Master windows"""
    def __init__(self):
        self.visuals = Visuals(self)
        self.graphic = Graphic(self.visuals)
        self.loader = Loader(self.visuals)
        self.osc = Osc(OSC_CORE, OSC_GUI)

        self.osc.listen('visual', self.cb_visual)
        self.osc.listen('audio', self.cb_audio)

        self.threads = [
            self.loader,
            self.osc
        ]
        self._stop = False

    def run(self):
        print 'starting pineal.core'
        for th in self.threads:
            th.start()
        try:
            while not self._stop:
                self.graphic.update()
        except KeyboardInterrupt:
            None

        self.threads.reverse()
        for th in self.threads:
            th.stop()

    def stop(self):
        print 'stopping pineal.core'
        self._stop = True

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
