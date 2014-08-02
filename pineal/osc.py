import threading
from thirdparty.OSC import OSCServer, OSCClient, OSCClientError, OSCMessage


class Osc(threading.Thread):
    def __init__(self, visuals):
        threading.Thread.__init__(self)

        self.server = OSCServer( ("localhost", 1420) )
        self.client = OSCClient()
        self.client.connect( ("localhost", 1421) )

        self.visuals = visuals
        self.paths = []
        self._stop = False

    def run(self):
        while not self._stop:
            self.updatePaths()
            self.server.handle_request()
        self.server.close()

    def callback(self, path, tags, args, source):
        print path, tags, args, source
        path = [s for s in path.split('/') if s]

        #/visual/var
        if len(path)==2:
            print 'setting visual variable'

        #/audioParamter
        if len(path)==1:
            print 'setting audio value'

    def stop(self):
        self._stop = True

    def updatePaths(self):
        paths = []
        for visual_k in self.visuals.keys():
            for var_k in self.visuals[visual_k].var.keys():
                paths.append(visual_k + '/' + var_k)

        for path in paths:
            if path not in self.paths:
                self.add(path)

        for path in self.paths:
            if path not in paths:
                self.remove(path)

    def add(self, path):
        self.paths.append(path)
        self.server.addMsgHandler(path, self.callback)
        try:
            self.client.send( OSCMessage('/add', path.split('/')) )
        except OSCClientError:
            None

    def remove(self, path):
        self.paths.remove(path)
        #self.server.delMsgHandler(path)
        try:
            self.client.send( OSCMessage('/remove', path.split('/')) )
        except OSCClientError:
            None
