import threading
from thirdparty.OSC import OSCServer, OSCClient, OSCClientError, OSCMessage
from pineal.config import OSC_CORE, OSC_GUI
import pineal.livecoding.audio


class Osc(threading.Thread):
    def __init__(self, visuals):
        threading.Thread.__init__(self)

        self.server = OSCServer(OSC_CORE)
        self.client = OSCClient()
        self.client.connect(OSC_GUI)

        for param in pineal.livecoding.audio.__dict__.keys():
            if param[0]!='_':
                self.server.addMsgHandler('/audio/'+param, self.callback)

        self.visuals = visuals
        self.paths = []
        self.var = {}
        self._stop = False

    def run(self):
        while not self._stop:
            self.update()
            self.server.handle_request()
        self.server.close()

    def callback(self, path, tags, args, source):
        #print path, tags, args, source
        path = [s for s in path.split('/') if s]
        value = args if len(tags)>1 else args[0]

        if not path:
            return

        #/visual_name/var_name
        if len(path)==3 and path[0]=='visual':
            path = path[1:]
            (visual,var) = path
            self.visuals[visual].set_var(var, value)
            self.var['/'.join(path)] = value
        #/audioParamter
        elif len(path)==2 and path[0]=='audio':
            (param,) = path[1:]
            pineal.livecoding.audio.__dict__[param] = value

    def stop(self):
        self._stop = True

    def update(self):
        var = {}
        for visual_k in self.visuals.keys():
            for k,v in self.visuals[visual_k].get_var():
                var[visual_k + '/' + k] = v

        for path,v in var.items():
            if path in self.var.keys():
                if v != self.var[path]:
                    self.var[path] = v
                    self.change(path, v)
            else:
                self.var[path] = v
                self.add(path)
                self.change(path, v)

        for path,v in self.var.items():
            if path not in var.keys():
                del self.var[path]
                self.remove(path)

    def add(self, path):
        self.server.addMsgHandler('/visual/'+path, self.callback)
        try:
            self.client.send( OSCMessage('/add', path.split('/')) )
        except OSCClientError:
            None

    def remove(self, path):
        #self.server.delMsgHandler(path)
        try:
            self.client.send( OSCMessage('/remove', path.split('/')) )
        except OSCClientError:
            None

    def change(self, path, val):
        try:
            self.client.send( OSCMessage('/change', path.split('/')+[val]) )
        except OSCClientError:
            None
