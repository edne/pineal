from threading import Thread
import gtk
from thirdparty.OSC import OSCClient, OSCServer, OSCMessage
from pineal.config import OSC_CORE, OSC_GUI

class GuiOsc(Thread):
    def __init__(self, gui):
        Thread.__init__(self)
        self.gui = gui

        self.server = OSCServer(OSC_GUI)
        self.server.addMsgHandler('/add', self.add)
        self.server.addMsgHandler('/remove', self.remove)
        self.server.addMsgHandler('/change', self.change)

        self.client = OSCClient()
        self.client.connect(OSC_CORE)

        self._stop = False

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self._stop = True

    def add(self, path, tags, args, source):
        self.gui.add(*args)

    def remove(self, path, tags, args, source):
        self.gui.remove(*args)

    def change(self, path, tags, args, source):
        self.gui.change(*args)

    def send_change(self, visual, var, value):
        self.client.send( OSCMessage('/visual/'+visual+'/'+var, float(value)) )

    def send_cmd(self, cmd):
        self.client.send( OSCMessage('/cmd/'+cmd) )
