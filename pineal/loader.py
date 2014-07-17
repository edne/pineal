from config import VISUALS_PATH

import threading, os
from glob import glob
from os.path import getmtime

import visuals


class Loader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)
        self._stop = False

    def run(self):
        while not self._stop:
            self.load()

            #time.sleep(0.01)

    def load(self):
        names = list()
        for filename in glob(os.path.join(self.path,'*.py')):
            name = os.path.basename(os.path.splitext(filename)[0])
            names.append(name)

        for v in visuals.get():
            if v.name not in names:
                v.remove()

        for name in names:
            v = visuals.get(name)

            path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)
            filename = os.path.join(path, name+'.py')

            if not v:
                v = visuals.Visual(name)
                visuals.add(v)
                v.filetime = 0

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

# TODO: that's HORRIBLE
thread = None


def init():
    global thread
    thread = Loader()


def start():
    thread.start()


def stop():
    thread.stop()
