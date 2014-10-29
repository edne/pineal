import threading
from thirdparty.OSC import OSCServer, OSCClient, OSCClientError, OSCMessage
from pineal.config import OSC_CORE, OSC_GUI
import pineal.livecoding.audio


class Osc(threading.Thread):
    def __init__(self, visuals):
        threading.Thread.__init__(self)

        self.visuals = visuals

        self.server = OSCServer(OSC_CORE)
        self.client = OSCClient()
        self.client.connect(OSC_GUI)
        self.server.addMsgHandler('default', self.callback)

        self.var = {}
        self._stop = False

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
            cbs[path[0]](value, *path[1:])

    def cb_visual(self, value, visual, var):
        self.visuals[visual].set_var(var, value)
        self.var['%s/%s' % (visual,var)] = value

    def cb_audio(self, value, key):
        pineal.livecoding.audio.__dict__[key] = value

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

    def add(self, path, val):
        self.client.send( OSCMessage('/add', path.split('/')+[val]) )
