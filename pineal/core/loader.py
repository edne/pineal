from pineal.config import VISUALS_PATH

import threading, os, time
from glob import glob
from os.path import getmtime


class Loader(threading.Thread):
    def __init__(self, visuals):
        self.visuals = visuals
        threading.Thread.__init__(self)

        self.path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)
        self._stop = False

    def run(self):
        while not self._stop:
            self.load()

            time.sleep(0.01)

    def load(self):
        names = [
            os.path.basename(os.path.splitext(filename)[0])
            for filename in glob(os.path.join(self.path,'*.py'))
        ]

        for name in self.visuals.keys():
            if name not in names:
                print 'removing'
                del self.visuals[name]

        for name in names:
            if name in self.visuals:
                v = self.visuals[name]
            else:
                v = self.visuals.new(name)
                v.filetime = 0

            path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)
            filename = os.path.join(path, name+'.py')

            try:
                filetime = getmtime(filename)
            except OSError:
                continue

            if filetime != v.filetime:
                print "loading "+name+".py"
                v.filetime = filetime
                try:
                    f = open(filename, "r")
                    code = f.read()
                    f.close()
                except IOError as e:
                    print e
                    return

                v.load(code)

    def stop(self):
        self._stop = True
