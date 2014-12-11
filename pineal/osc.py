import threading
from thirdparty.OSC import OSCServer, OSCClient, OSCClientError, OSCMessage


class Osc(threading.Thread):
    def __init__(self, port_in=None, port_out=None):
        threading.Thread.__init__(self)

        if port_in:
            self.server = OSCServer(port_in)
            self.server.addMsgHandler('default', self.callback)

        if port_out:
            self.client = OSCClient()
            self.client.connect(port_out)

        self.cbs = {}
        self._stop = False

    def run(self):
        while not self._stop:
            self.server.handle_request()
        self.server.close()

    def listen(self, key, cb):
        self.cbs[key] = cb

    def callback(self, path, tags, args, source):
        _path = [s for s in path.split('/') if s]

        if _path[0] in self.cbs.keys():
            self.cbs[_path[0]](path, tags, args, source)

    def stop(self):
        self._stop = True

    def send(self, path, *args):
        try:
            self.client.send( OSCMessage(path, args) )
        except OSCClientError:  # sometime rises a 'connection refused'
            pass
