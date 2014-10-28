import threading
from thirdparty.OSC import OSCServer, OSCClient, OSCClientError, OSCMessage
from pineal.config import OSC_CORE, OSC_GUI
import pineal.livecoding.audio


class Osc(threading.Thread):
    def __init__(self, core, visuals):
        threading.Thread.__init__(self)

        self.core = core
        self.visuals = visuals
        self.paths = []
        self.var = {}
        self._stop = False

        self.server = OSCServer(OSC_CORE)
        self.client = OSCClient()
        self.client.connect(OSC_GUI)

        for param in pineal.livecoding.audio.__dict__.keys():
            if param[0]!='_':
                self.server.addMsgHandler('/audio/'+param, self.callback)

    def run(self):
        while not self._stop:
            self.update()
            self.server.handle_request()
        self.server.close()

    def callback(self, path, tags, args, source):
        path = [s for s in path.split('/') if s]
        value = (args if tags[1:] else args[0]) if args else None

        cbs = {
            'visual': self.cb_visual,
            'audio': self.cb_audio,
        }

        if path[1:] and path[0] in cbs.keys():
            cbs[path[0]](path[1:], value)

    def cb_visual(self, path, value):
        (visual,var) = path
        self.visuals[visual].set_var(var, value)
        self.var['/'.join(path)] = value

    def cb_audio(self, path, value):
        pineal.livecoding.audio.__dict__[path[0]] = value

    def stop(self):
        self._stop = True

    def update(self):
        var = {}
        for visual_k in self.visuals.keys():
            for k,v in self.visuals[visual_k].get_var():
                var[visual_k + '/' + k] = v

        for path,v in var.items():
            if not path in self.var.keys():
                self.var[path] = v
                self.add(path, v)

        for path,v in self.var.items():
            if path not in var.keys():
                del self.var[path]
                self.remove(path)

    def add(self, path, val):
        self.server.addMsgHandler('/visual/'+path, self.callback)
        try:
            self.client.send( OSCMessage('/add', path.split('/')+[val]) )
        except OSCClientError:
            None
