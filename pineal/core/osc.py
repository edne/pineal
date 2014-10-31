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

        self._stop = False

    def run(self):
        while not self._stop:
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
        self.visuals[visual][var] = value

    def cb_audio(self, value, key):
        pineal.livecoding.audio.__dict__[key] = value

    def stop(self):
        self._stop = True

    def send(self, path, *args):
        try:
            self.client.send( OSCMessage('/'+path, args) )
        except OSCClientError:  # sometime rises a 'connection refused'
            pass
