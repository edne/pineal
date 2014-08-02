from multiprocessing import Process

from visuals import Visuals
from graphic import Graphic
from loader import Loader
from analyzer import Analyzer
from osc import Osc


class Core(Process):
    def __init__(self):
        Process.__init__(self)

        visuals = Visuals()
        self.graphic = Graphic(visuals)

        self.threads = [
            Loader(visuals),
            Analyzer(visuals),
            Osc(visuals)
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
