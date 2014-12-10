import os
from threading import Thread
from time import sleep
from glob import glob
from os.path import getmtime

from pineal.osc import Osc
from pineal.config import VISUALS_PATH, OSC_CORE


class Loader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.times = {}

        self.path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)

        self.osc = Osc(port_out = OSC_CORE)
        self._stop = False

    def run(self):
        print 'starting pineal.loader'
        sleep(1)  # TODO add intelligent 'wait for other modules' system
        while not self._stop:
            self.load()
            sleep(0.01)

    def load(self):
        names = (
            os.path.basename(os.path.splitext(filename)[0])
            for filename in glob(os.path.join(self.path,'*.py'))
        )

        for name in names:
            if name not in self.times.keys():
                self.times[name] = 0

            path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)
            filename = os.path.join(path, name+'.py')

            try:
                filetime = getmtime(filename)
            except OSError:
                pass

            if filetime != self.times[name]:
                print "loading "+name+".py"
                self.times[name] = filetime
                try:
                    f = open(filename, "r")
                    code = f.read()
                    f.close()
                except IOError as e:
                    print e
                    return

                self.osc.send('/code/'+name, code)

    def stop(self):
        self._stop = True
